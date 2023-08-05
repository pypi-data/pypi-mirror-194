"""

Typical usage example:

    disk: DiskStorage = DiskStore(file_name="books.db")
    disk.set(key="othello", value="shakespeare")
    author: str = disk.get("othello")
    # it also supports dictionary style API too:
    disk["hamlet"] = "shakespeare"
"""
import os.path
import time
import typing

from .config import WRITE_CONSISTENCY
from .config import ConsistencyMode
from .record import HEADER_SIZE
from .record import KeyEntry
from .record import decode_header
from .record import decode_kv
from .record import encode_kv
from .record import format_key
from .record import random_string

DEFAULT_WHENCE: typing.Final[int] = 0  # beginning of the file


# DiskStorage is a Log-Structured Hash Table as described in the BitCask paper. We
# keep appending the data to a file, like a log. DiskStorage maintains an in-memory
# hash table called KeyDir, which keeps the row's location on the disk.
#
# The idea is simple yet brilliant:
#   - Write the record to the disk
#   - Update the internal hash table to point to that byte offset
#   - Whenever we get a read request, check the internal hash table for the address,
#       fetch that and return
#
# KeyDir does not store values, only their locations.
#
# The above approach solves a lot of problems:
#   - Writes are insanely fast since you are just appending to the file
#   - Reads are insanely fast since you do only one disk seek. In B-Tree backed
#       storage, there could be 2-3 disk seeks
#
# However, there are drawbacks too:
#   - We need to maintain an in-memory hash table KeyDir. A database with a large
#       number of keys would require more RAM
#   - Since we need to build the KeyDir at initialisation, it will affect the startup
#       time too
#   - Deleted keys need to be purged from the file to reduce the file size
#
# Read the paper for more details: https://riak.com/assets/bitcask-intro.pdf


class HadroDB:
    """
    Implements the KV store on the disk

    Args:
        file_name (str): name of the file where all the data will be written. Just
            passing the file name will save the data in the current directory. You may
            pass the full file location too.

    Attributes:
        file_name (str): name of the file where all the data will be written. Just
            passing the file name will save the data in the current directory. You may
            pass the full file location too.
        file (typing.BinaryIO): file object pointing the file_name
        write_position (int): current cursor position in the file where the data can be
            written
        key_dir (dict[str, KeyEntry]): is a map of key and KeyEntry being the value.
            KeyEntry contains the position of the byte offset in the file where the
            value exists. key_dir map acts as in-memory index to fetch the values
            quickly from the disk
    """

    def __init__(self, collection: typing.Union[str, None] = None):
        import logging

        logging.warning("HadroDB is experimental and not recommended for use.")
        self.collection: str = collection
        self.file_name: str = collection + "/00000000.hadro"
        self.write_position: int = 0
        self.key_dir: dict[bytes, KeyEntry] = {}

        if collection is None:
            raise ValueError("HadroDB requires a collection name")
        # if the collection exists, it must be a folder, not a file
        if os.path.exists(collection):
            if not os.path.isdir(collection):
                raise ValueError("Collection must be a folder")
            # if the file exists already, then we will load the key_dir
            self._init_key_dir()
        else:
            os.makedirs(collection, exist_ok=True)

        # we open the file in `a+b` mode:
        # a - says the writes are append only. `a+` means we want append and read
        # b - says that we are operating the file in binary mode (as opposed to the
        #     default string mode)
        self.file: typing.BinaryIO = open(self.file_name, "a+b")
        self.fileno = self.file.fileno()

    def set(self, key: typing.Union[bytes, str], value: typing.Any) -> None:
        """
        set stores the key and value on the disk

        Args:
            key (str): the key
            value (str): the value
        """
        # The steps to save a KV to disk is simple:
        # 1. Encode the KV into bytes
        # 2. Write the bytes to disk by appending to the file
        # 3. Update KeyDir with the KeyEntry of this key
        timestamp: int = int(time.time())
        key = format_key(key)
        size, data = encode_kv(timestamp=timestamp, key=key, value=value)
        # notice we don't do file seek while writing
        self._write(data)
        kv: KeyEntry = KeyEntry(timestamp=timestamp, position=self.write_position, total_size=size)
        self.key_dir[key] = kv
        # update last write position, so that next record can be written from this point
        self.write_position += size

    def add(self, value: typing.Any) -> bytes:
        """
        Adds a value to the store and lets the system create the key.
        """
        key = random_string()
        self.set(key=key, value=value)
        return key

    def get(
        self,
        key: typing.Union[bytes, str],
        default: typing.Union[None, typing.Any] = None,
    ) -> typing.Any:
        """
        get retrieves the value from the disk and returns. If the key does not exist
        then it returns an empty string

        Args:
            key (str): the key

        Returns:
            string
        """
        # How get works?
        # 1. Check if there is any KeyEntry record for the key in KeyDir
        # 2. Return an empty string if key doesn't exist
        # 3. If it exists, then read KeyEntry.total_size bytes starting from the
        #    KeyEntry.position from the disk
        # 4. Decode the bytes into valid KV pair and return the value
        key = format_key(key)
        record: typing.Optional[KeyEntry] = self.key_dir.get(key)
        if record is None:
            if default is not None:
                return default
            raise IndexError(key)
        #  move the current pointer to the right offset
        self.file.seek(record.position, DEFAULT_WHENCE)
        data: bytes = self.file.read(record.total_size)
        _, _, value = decode_kv(data)
        return value

    def _write(self, data: bytes) -> None:
        # saving stuff to a file reliably is hard!
        # if you would like to explore and learn more, then
        # start from here: https://danluu.com/file-consistency/
        # and read this too: https://lwn.net/Articles/457667/
        os.write(self.fileno, data)

        if WRITE_CONSISTENCY == ConsistencyMode.AGGRESSIVE:
            # calling fsync after every write is important, this assures that our writes
            # are actually persisted to the disk
            os.fsync(self.fileno)

    def _init_key_dir(self) -> None:
        # we will initialise the key_dir by reading the contents of the file, record by
        # record. As we read each record, we will also update our KeyDir with the
        # corresponding KeyEntry
        #
        # NOTE: this method is a blocking one, if the DB size is huge then it will take
        # a lot of time to startup

        """
        # TODO
        - Load the primary.key file, this is a B-TREE
        - Hash the data file
        - this primary.key file has a hash of the data file
        - if the hashes match, just use the BTREE as the index
        - if the hashes don't match, rebuild the BTREE from scratch
        """

        print("****----------initialising the database----------****")
        with open(self.file_name, "rb") as f:
            while header_bytes := f.read(HEADER_SIZE):
                timestamp, key_size, value_size = decode_header(data=header_bytes)
                key = f.read(key_size)
                value_bytes = f.read(value_size)  # we don't use this value but read it
                # value = value_bytes.decode("utf-8")
                total_size = HEADER_SIZE + key_size + value_size
                kv = KeyEntry(
                    timestamp=timestamp,
                    position=self.write_position,
                    total_size=total_size,
                )
                self.key_dir[key] = kv
                self.write_position += total_size
        #                print(f"loaded k={key}, v={value}")
        print("****----------initialisation complete----------****")

    def keys(self) -> typing.Tuple[bytes, ...]:
        return tuple(self.key_dir.keys())

    def close(self) -> None:
        # before we close the file, we need to safely write the contents in the buffers
        # to the disk. Check documentation of DiskStorage._write() to understand
        # following the operations
        self.file.flush()
        os.fsync(self.fileno)
        self.file.close()

    def __setitem__(self, key: typing.Union[bytes, str], value: typing.Any) -> None:
        return self.set(key, value)

    def __getitem__(self, item: typing.Union[bytes, str, typing.Iterable]) -> typing.Any:
        if isinstance(item, (list, set, tuple, typing.KeysView)):
            list_of_docs = []
            for individual_key in item:
                this_doc = self.get(individual_key)
                list_of_docs.append(this_doc)
            return list_of_docs
        # ignore the typing error, we've dealt with the iterables above
        return self.get(item)  # type:ignore

    def __len__(self):
        return len(self.key_dir)
