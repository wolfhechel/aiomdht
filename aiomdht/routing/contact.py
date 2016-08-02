import socket

from ..node_id import NodeID


class Contact(object):

    node_id = None

    address = None

    port = None

    def __init__(self, node_id, address, port):
        self.node_id = node_id
        self.address = address
        self.port = port

    @classmethod
    def from_compact_node_info(cls, bytes):
        if len(bytes) < 26:
            raise ValueError('Not enough data for a compact node info structure')

        node_id = NodeID(bytes[:20])
        address = socket.inet_ntoa(bytes[20:24])
        port = int.from_bytes(bytes[24:], byteorder='big')

        return cls(node_id, address, port)

    def __repr__(self):
        return "<%s> (%s:%d)" % (
            self.node_id.hex.decode('utf-8'),
            self.address,
            self.port
        )