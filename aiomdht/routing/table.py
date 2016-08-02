from .kbucket import KBucket


class RoutingTable(object):

    local_node_id = None

    root = None

    def __init__(self, local_node_id):
        self.local_node_id = local_node_id

        self.root = KBucket(self)
