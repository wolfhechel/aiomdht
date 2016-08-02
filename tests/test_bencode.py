import pytest

from aiomdht import bencode


def describe_encode():

    def encode_integer():
        assert bencode.encode(42) == b'i42e'
        assert bencode.encode(0) == b'i0e'
        assert bencode.encode(-12) == b'i-12e'

    def encode_bytes():
        assert bencode.encode(b'test') == b'4:test'
        assert bencode.encode(b'') == b'0:'

    def encode_string():
        assert bencode.encode('åäö') == b'6:\xc3\xa5\xc3\xa4\xc3\xb6'
        assert bencode.encode('test') == b'4:test'

    def encode_list():
        assert bencode.encode([42, b'test', 'test']) == b'li42e4:test4:teste'
        assert bencode.encode([42, [b'test']]) == b'li42el4:testee'

    def encode_dictionary():
        assert bencode.encode({
            b'i': 42,
            b'b': b'a',
            b'l': [1, b'a']
        }) == b'd1:b1:a1:ii42e1:lli1e1:aee'

    def encode_dictionary_keyerror_on_none_byte_key():
        with pytest.raises(KeyError):
            bencode.encode({
                1: b'test'
            })


def describe_decode():

    def decode_integer():
        assert bencode.decode(b'i42e') == 42
        assert bencode.decode(b'i-42e') == -42
        assert bencode.decode(b'i0e') == 0

    def decode_bytes():
        assert bencode.decode(b'4:test') == b'test'
        assert bencode.decode(b'0:') == b''
        assert bencode.decode(b'6:\xc3\xa5\xc3\xa4\xc3\xb6') == b'\xc3\xa5\xc3\xa4\xc3\xb6'

    def decode_list():
        assert bencode.decode(b'li42e4:testli1eee') == [42, b'test', [1]]

    def decode_dictionary():
        assert bencode.decode(b'd1:b4:test1:ii42e1:lli1eee') == bencode.OrderedDict(
            (
                (b'b', b'test'),
                (b'i', 42),
                (b'l', [1])
            )
        )
