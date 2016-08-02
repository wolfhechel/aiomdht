class KBucket(object):

    low = None

    high = None

    bucket = None

    local_node_id = None

    k = None

    bit_index = 0

    can_split = True

    def __init__(self, local_node_id, k=8, bit_index=0):
        self.local_node_id = local_node_id
        self.bucket = set()
        self.k = k
        self.bit_index = bit_index

    @property
    def is_split(self):
        return self.bucket is None

    @property
    def number_of_contacts(self):
        return len(self.bucket) if not self.is_split else None

    def construct_new_bucket(self):
        return KBucket(
            self.local_node_id,
            k=self.k,
            bit_index=self.bit_index + 1
        )

    def bucket_for_contact(self, new_contact):
        if new_contact.node_id.bit_set(self.bit_index):
            new_bucket = self.high
        else:
            new_bucket = self.low

        return new_bucket

    def add(self, new_contact):
        if not self.is_split:
            if self.number_of_contacts == self.k: # Time to split!
                if self.can_split:
                    self.low = self.construct_new_bucket()
                    self.high = self.construct_new_bucket()

                    if self.local_node_id.bit_set(self.bit_index + 1):
                        home_bucket = self.high
                        away_bucket = self.low
                    else:
                        home_bucket = self.low
                        away_bucket = self.high

                    home_bucket.can_split = True
                    away_bucket.can_split = False

                    for contact in self.bucket:
                        self.bucket_for_contact(contact).add(contact)

                    self.bucket = None
                    self.add(new_contact)
            else:
                self.bucket.add(new_contact)
        else:
            self.bucket_for_contact(new_contact).add(new_contact)
