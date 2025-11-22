"""
This module provides a fake backend implementation for testing purposes.
It simulates MongoDB operations using in-memory data structures.
"""

from unittest.mock import MagicMock


def fake_ask_model(messages):
    """
    fake implementation of ask_model that return a string
    """
    return "assistant reply"


"""
Fake collection class to simulate MongoDB collection operations.
"""


class FakeCollection:
    def __init__(self):
        """
        Initialize an empty collection.
        """
        self.data = []
        self.counter = 0

    def reset(self):
        """
        Reset the collection to empty state.
        """
        self.data.clear()
        self.counter = 0

    def insert_one(self, doc):
        """
        insert a document into the collection.
        """
        doc = dict(doc)

        if "_id" not in doc:
            self.counter += 1
            doc["_id"] = str(self.counter)

        self.data.append(doc)
        return MagicMock(inserted_id=doc["_id"])

    def find_one(self, filt):
        """
        find one document matching the filter.
        """
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                return doc
        return None

    def find(self, filt=None):
        """
        find all documents matching the filter.

        """
        if filt is None:
            return list(self.data)
        return [d for d in self.data if all(d.get(k) == v for k, v in filt.items())]

    def update_one(self, filt, update_data):
        """
        update one document matching the filter.
        """
        modified = 0
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                doc.update(update_data["$set"])
                modified = 1
        return MagicMock(modified_count=modified)

    def delete_one(self, filt):
        """
        delete one document matching the filter.
        """
        deleted = 0
        for i, doc in enumerate(self.data):
            if all(doc.get(k) == v for k, v in filt.items()):
                del self.data[i]
                deleted = 1
                break
        return MagicMock(deleted_count=deleted)


"""
Fake database class to hold fake collections.
"""


class FakeDB:
    def __init__(self):
        """
        Initialize the fake database with chats and messages collections.
        """
        self.chats = FakeCollection()
        self.messages = FakeCollection()

    def reset(self):
        """
        reset both collections.
        """
        self.chats.reset()
        self.messages.reset()
