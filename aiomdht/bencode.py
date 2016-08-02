from io import BytesIO
from collections import OrderedDict


def encode_integer(value):
    return ('i%de' % value).encode('ascii')


def encode_bytes(value):
    return (b'%d:' % len(value)) + value


def encode_string(value):
    return encode_bytes(value.encode('utf-8'))


def encode_list(value):
    list_encoded = b''.join([encode(v) for v in value])

    return b'l' + list_encoded + b'e'


def encode_dictionary(value):
    dict_encoded = b'd'

    for key in sorted(value.keys()):
        if not isinstance(key, bytes):
            raise KeyError('Key %r is not a bytes type' % key)

        val = value[key]

        dict_encoded += encode_bytes(key)
        dict_encoded += encode(val)

    dict_encoded += b'e'

    return dict_encoded


encode_map = (
    (int, encode_integer),
    (bytes, encode_bytes),
    (str, encode_string),
    (list, encode_list),
    (dict, encode_dictionary)
)


def encode(value):
    for type_, encoder in encode_map:
        if isinstance(value, type_):
            return encoder(value)


def decode_integer(buff):
    int_val = b''

    while True:
        byte = buff.read(1)
        if byte != b'e':
            int_val += byte
        else:
            return int(int_val)


byte_int_range = bytearray(range(48, 57))


def decode_list(buff):
    values = []

    marker = buff.read(1)

    while marker != b'e':
        values.append(_decode_from_marker(buff, marker))
        marker = buff.read(1)

    return values


def decode_dictionary(buff):
    dictionary = OrderedDict()

    marker = buff.read(1)

    while marker != b'e':
        key = decode_bytes(buff, marker)

        value = _decode_from_marker(buff, buff.read(1))

        dictionary[key] = value

        marker = buff.read(1)

    return dictionary


bytes_length_end_marker = ord(b':')


def decode_bytes(buff, bytes_length):
    while bytes_length[-1] != bytes_length_end_marker:
        bytes_length += buff.read(1)

    number_of_bytes = int(bytes_length[:-1])

    return buff.read(number_of_bytes)


def _decode_from_marker(buff, marker):
    if marker == b'i':
        val = decode_integer(buff)
    elif marker == b'l':
        val = decode_list(buff)
    elif marker == b'd':
        val = decode_dictionary(buff)
    elif marker in byte_int_range:
        val = decode_bytes(buff, marker)
    else:
        raise ValueError()

    return val


def decode_buff(buff):
    byte = buff.read(1)

    val = _decode_from_marker(buff, byte)

    return val


def decode(value):
    data = BytesIO(value)

    val = decode_buff(data)

    data.close()

    return val
