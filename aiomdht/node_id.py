import os

import binascii


class NodeID(object):

    node_id = None

    def __init__(self, node_id):
        self.node_id = node_id

    @classmethod
    def random(cls):
        random_node_id = os.urandom(20)

        return cls(random_node_id)

    def bit_set(self, bit):
        bit_index_in_byte = bit % 8

        byte_index = int((bit - bit_index_in_byte) / 8)

        return bool(self.node_id[byte_index] & (1 << (7 - bit_index_in_byte)))

    def __bytes__(self):
        return self.node_id

    def __int__(self):
        return int.from_bytes(
            self.node_id,
            byteorder='big'
        )

    def __eq__(self, other):
        return self.node_id == other.node_id

    @property
    def hex(self):
        return binascii.hexlify(self.node_id)

    def __repr__(self):
        return "<NodeID %s>" % self.hex