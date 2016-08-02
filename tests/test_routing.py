import sys

import pytest

from aiomdht.node_id import NodeID
from aiomdht.routing import Contact, KBucket

def describe_contact():

    def from_compact_node_info_bad_data_value_error():
        with pytest.raises(ValueError):
            Contact.from_compact_node_info(b'\xca\xe8\xc8fm\x9d\x82\x88')

    def from_compat_node_info():
        contact = Contact.from_compact_node_info(
            b'\xca\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        assert contact.node_id == NodeID(b'\xca\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-')
        assert contact.address == '203.0.113.1'
        assert contact.port == 1234

    def contact_is_identifiable_in_set():
        contacts = set()

        contact = Contact.from_compact_node_info(
            b'\xca\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        contacts.add(contact)

        assert contact in contacts


def describe_kbucket():

    local_node_id = NodeID(b'\xff\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-')

    def adding_contact_to_bucket_works():
        bucket = KBucket(local_node_id)

        contact = Contact.from_compact_node_info(
            b'\xca\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(contact)

        assert contact in bucket.bucket
        assert bucket.number_of_contacts == 1

    def adding_k_contacts_to_bucket_does_not_split():
        bucket = KBucket(local_node_id)

        for i in range(bucket.k):
            prefix = i.to_bytes(length=1, byteorder=sys.byteorder)

            contact = Contact.from_compact_node_info(
                prefix + b'\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
            )

            bucket.add(contact)

        assert bucket.bucket is not None
        assert bucket.high is None
        assert bucket.low is None

    def adding_k_contacts_plus_one_splits_bucket():
        bucket = KBucket(local_node_id)

        for i in range(bucket.k + 1):
            prefix = i.to_bytes(length=1, byteorder=sys.byteorder)

            contact = Contact.from_compact_node_info(
                prefix + b'\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
            )

            bucket.add(contact)

        assert bucket.bucket is None
        assert isinstance(bucket.high, KBucket)
        assert isinstance(bucket.low, KBucket)

    def bucket_splitting_redistributes_bucket():
        bucket = KBucket(local_node_id, k=2)

        low_contact = Contact.from_compact_node_info(
            b'\x00\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        high_contact = Contact.from_compact_node_info(
            b'\xff\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(low_contact)
        bucket.add(high_contact)

        new_contact = Contact.from_compact_node_info(
            b'\x80\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(new_contact)

        assert low_contact in bucket.low.bucket
        assert high_contact in bucket.high.bucket
        assert new_contact in bucket.high.bucket

    def splitting_is_iterative():
        bucket = KBucket(local_node_id, k=2)

        first_contact = Contact.from_compact_node_info(
            b'\xd0\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        second_contact = Contact.from_compact_node_info(
            b'\xd8\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        third_contact = Contact.from_compact_node_info(
            b'\xe0\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(first_contact)
        bucket.add(second_contact)
        bucket.add(third_contact)

        assert first_contact in bucket.high.high.low.bucket
        assert second_contact in bucket.high.high.low.bucket
        assert third_contact in bucket.high.high.high.bucket

    def bucket_add_redistributes_if_split():
        bucket = KBucket(local_node_id, k=2)

        bucket.add(Contact.from_compact_node_info(
            b'\x00\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        ))

        bucket.add(Contact.from_compact_node_info(
            b'\x01\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        ))

        bucket.add(Contact.from_compact_node_info(
            b'\x02\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        ))

        # Now add another contact and make sure it's added to the right bucket

        new_contact = Contact.from_compact_node_info(
            b'\x80\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(new_contact)

        assert new_contact in bucket.high.bucket

    def bucket_does_not_split_unless_local_node_id_in_bucket(): # God I love long method names
        bucket = KBucket(local_node_id, k=2)

        first_contact = Contact.from_compact_node_info(
            b'\x60\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        second_contact = Contact.from_compact_node_info(
            b'\x40\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        third_contact = Contact.from_compact_node_info(
            b'\x70\xe8\xc8fm\x9d\x82\x88&I\x0c[\xce\xc5\x94\xeds\xc5r-\xcb\x00q\x01\x04\xd2'
        )

        bucket.add(first_contact)
        bucket.add(second_contact)
        bucket.add(third_contact)

        assert first_contact in bucket.low.bucket
        assert second_contact in bucket.low.bucket

        assert third_contact not in bucket.low.bucket
