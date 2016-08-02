from aiomdht.node_id import NodeID


def describe_node_id():

    def test_node_id_equality():
        assert NodeID(b'123') == NodeID(b'123')

    def test_bit_is_set():
        node_id = NodeID((0b10100000).to_bytes(1, byteorder='big'))
        assert node_id.bit_set(0) == True
        assert node_id.bit_set(1) == False
        assert node_id.bit_set(2) == True