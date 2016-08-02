from asyncio import DatagramProtocol


class DHTProtocol(DatagramProtocol):
    """ DHT protocol class used in conjunction with
    `asyncio.create_datagram_endpoint()`

    This is the main protocol abstraction providing the entire API interface
    for the DHT.

    Attributes:
        routing_table (:obj:`RoutingTable`) Routing Table for our DHT node

    """

    routing_table = None

    def __init__(self, routing_table):
        self.routing_table = routing_table

    async def bootstrap(self, address, port):
        """ Used to bootstrap our DHT node against another DHT node.

        The bootstrapping proceadure is made up of our node contactinc
        the bootstraping node, querying it for any nodes close to us.

        The returned nodes are propagated into our routing table which
        we in the next run uses to find any closer nodes to us,
        these nodes are then contacted and queried in the same way.

        This process is looped over until we cannot find closer nodes than
        the ones we already keep in our routing table.

        Args:
            address (str): DHT node address
            port (int): DHT node port
        """
        pass

    async def ping(self, address, port):
        """ Sends a ping query to the specified contact.

        Args:
            address (str): Address of the DHT node to ping
            port (int): Port of the DHT node to ping

        Returns:
            NodeID if DHT node responded to the ping

        Raises:
            TimeoutError: If no response is received from the DHT node within
            the given time.
        """

    async def find_node(self, node_id):
        """ Starts a lookup for node with id `node_id`

        Args:
            node_id (:obj:`NodeID`): NodeID of the node we're trying to find.

        Returns:
            `async` True if the node was found, False otherwise
        """

    async def get_peers(self, infohash):
        """ Starts a lookup to find peers for torrent with the given infohash.

        Args:
            infohash (bytes): infohash to find peers for

        Returns:
            `async` Array with peers for the given infohash and a token for announce_peer.
        """

    async def announce_peer(self, token):
        pass