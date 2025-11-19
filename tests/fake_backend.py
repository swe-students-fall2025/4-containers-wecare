from unittest.mock import MagicMock

# A fake implementation of ask_model for testing purposes
def fake_ask_model(messages):
    return "assistant reply"

# A fake in-memory database to simulate MongoDB operations
class FakeCollection:
    def __init__(self):
        self.data = []
        self.counter = 0

    def reset(self):
        self.data.clear()
        self.counter = 0

    def insert_one(self, doc):
        doc = dict(doc)

        if "_id" not in doc:
            self.counter += 1
            doc["_id"] = str(self.counter)

        self.data.append(doc)
        return MagicMock(inserted_id=doc["_id"])

    def find_one(self, filt):
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                return doc
        return None

    def find(self, filt=None):
        if filt is None:
            return list(self.data)
        return [d for d in self.data if all(d.get(k) == v for k, v in filt.items())]

    def update_one(self, filt, update_data):
        modified = 0
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                doc.update(update_data["$set"])
                modified = 1
        return MagicMock(modified_count=modified)

    def delete_one(self, filt):
        deleted = 0
        for i, doc in enumerate(self.data):
            if all(doc.get(k) == v for k, v in filt.items()):
                del self.data[i]
                deleted = 1
                break
        return MagicMock(deleted_count=deleted)


class FakeDB:
    def __init__(self):
        self.chats = FakeCollection()
        self.messages = FakeCollection()

    def reset(self):
        self.chats.reset()
        self.messages.reset()
