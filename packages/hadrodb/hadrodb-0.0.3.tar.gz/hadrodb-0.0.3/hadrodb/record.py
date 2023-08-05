"""
format module provides encode/decode functions for serialisation and deserialisation
operations

format module is generic and does not have any disk or memory specific code.

The disk storage deals with bytes; you cannot just store a string or object without
converting it to bytes. The programming languages provide abstractions where you
don't have to think about all this when storing things in memory (i.e. RAM).
Consider the following example where you are storing stuff in a hash table:

    books = {}
    books["hamlet"] = "shakespeare"
    books["anna karenina"] = "tolstoy"

In the above, the language deals with all the complexities:

    - allocating space on the RAM so that it can store data of `books`
    - whenever you add data to `books`, convert that to bytes and keep it in the memory
    - whenever the size of `books` increases, move that to somewhere in the RAM so that
      we can add new items

Unfortunately, when it comes to disks, we have to do all this by ourselves, write
code which can allocate space, convert objects to/from bytes and many other operations.

format module provides two functions which help us with serialisation of data.

    encode_kv - takes the key value pair and encodes them into bytes
    decode_kv - takes a bunch of bytes and decodes them into key value pairs

"""
import base64
import random
import struct
import typing

from cityhash import CityHash32
from cityhash import CityHash64
from ormsgpack import packb
from ormsgpack import unpackb

# Our key value pair, when stored on disk looks like this:
#   ┌───────────┬──────────┬────────────┬─────┬───────┐
#   │ timestamp │ key_size │ value_size │ key │ value │
#   └───────────┴──────────┴────────────┴─────┴───────┘
#
# This is analogous to a typical database's row (or a record). The total length of
# the row is variable, depending on the contents of the key and value.
#
# The first three fields form the header:
#   ┌───────────────┬──────────────┬────────────────┐
#   │ timestamp(4B) │ key_size(4B) │ value_size(4B) │
#   └───────────────┴──────────────┴────────────────┘
#
# These three fields store unsigned integers of size 4 bytes, giving our header a
# fixed length of 12 bytes. Timestamp field stores the time the record we
# inserted in unix epoch seconds. Key size and value size fields store the length of
# bytes occupied by the key and value. The maximum integer
# stored by 4 bytes is 4,294,967,295 (2 ** 32 - 1), roughly ~4.2GB. So, the size of
# each key or value cannot exceed this. Theoretically, a single row can be as large
# as ~8.4GB.
#
# We use `struct.pack` method to serialise our header to bytes. `struct.pack` function
# looks like this:
#
#   struct.pack(format, v1, v2, ...) -> bytes
#
# The first argument is a format string, which specifies how the parameters v1, v2, ...
# should be encoded. `HEADER_FORMAT` is our format string for the header.
# Check the struct documentation https://docs.python.org/3/library/struct.html
# to understand how to construct such a string.
#
# `<` - lil endian to be used to encode the integer
# `L` - represents long unsigned int (4 bytes). We have three fields, hence `LLL`
HEADER_FORMAT: typing.Final[str] = "<LLL"
HEADER_SIZE: typing.Final[int] = 12


def random_string():
    """
    Create a 16 character random string.
    """
    bytestring = struct.pack("=QL", random.getrandbits(64), random.getrandbits(32))
    return base64.b64encode(bytestring)


class KeyEntry:
    """
    KeyEntry keeps the metadata about the KV, specially the position of
    the byte offset in the file. Whenever we insert/update a key, we create a new
    KeyEntry object and insert that into KeyDir.

    Args:
        timestamp (int): Timestamp at which we wrote the KV pair to the disk. The value
            is current time in seconds since the epoch.
        position (int): The position is the byte offset in the file where the data
            exists
        total_size(int): Total size of bytes of the value. We use this value to know
            how many bytes we need to read from the file
    """

    slots = "timestamp", "position", "total_size"

    def __init__(self, timestamp: int, position: int, total_size: int):
        self.timestamp: int = timestamp
        self.position: int = position
        self.total_size: int = total_size


def format_key(key: typing.Union[bytes, str]) -> bytes:
    if isinstance(key, str):
        key = key.encode()
    if not isinstance(key, bytes):
        raise ValueError("HadroDB keys must be strings or byte strings.")

    if len(key) != 16:
        # We want a 96 bit hash, but CityHash doesn't support
        # Adding a 64 + 32 is faster then 3 x 32 or 2 x 64 or 1 x 128
        bits64 = CityHash64(key)
        bits32 = CityHash32(key)
        key = struct.pack("<QL", bits64, bits32)
        return base64.b64encode(key)

    return key


def encode_kv(timestamp: int, key: bytes, value: typing.Any) -> typing.Tuple[int, bytes]:
    """
    encode_kv encodes the KV pair into bytes

    Args:
        timestamp (int): Timestamp at which we wrote the KV pair to the disk. The value
            is current time in seconds since the epoch.
        key (str): the key (cannot exceed the maximum size)
        value (str): the value (cannot exceed the maximum size)

    Returns:
        tuple containing the size of encoded bytes and the byte object

    Raises:
        struct.error when parameters don't match the specific type / size
    """
    binary_data = packb(value)
    header: bytes = struct.pack(HEADER_FORMAT, timestamp, len(key), len(binary_data))
    data: bytes = key + binary_data
    return HEADER_SIZE + len(data), header + data


def decode_kv(data: bytes) -> typing.Tuple[int, bytes, bytes]:
    """
    decode_kv decodes the data bytes into appropriate KV pair

    Args:
        data (bytes): byte object containing the encoded KV data

    Returns:
        A tuple containing:

            timestamp (int): timestamp in epoch seconds
            key (str): the key
            value (str): the value

    Raises:
        struct.error: when parameters don't match the specific type / size
        IndexError: if the length of bytes is shorter than expected
        UnicodeDecodeError: if the key or values bytes could not be decoded to string
    """
    timestamp, key_size, value_size = decode_header(data[:HEADER_SIZE])
    key_bytes: bytes = data[HEADER_SIZE : HEADER_SIZE + key_size]
    value_bytes: bytes = data[HEADER_SIZE + key_size :]
    key: bytes = key_bytes
    value: bytes = unpackb(value_bytes)
    return timestamp, key, value


def decode_header(data: bytes) -> typing.Tuple[int, int, int]:
    """
    decode_header decodes the bytes into header using the `HEADER_FORMAT` format
    string

    Args:
        data (bytes): byte object containing the encoded header data

    Returns:
        A tuple containing:

            timestamp (int): timestamp in epoch seconds
            key_size (int): size of the key
            value_size (int): size of the value

    Raises:
        struct.error: when parameters don't match the specific type / size
    """
    timestamp, key_size, value_size = struct.unpack(HEADER_FORMAT, data)
    return timestamp, key_size, value_size
