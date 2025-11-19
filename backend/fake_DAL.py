#fake database to simulate MongoDB operations for testing
class FakeCollection:
    def __init__(self):
        self.data = []
        self.auto_id = 1

    def insert_one(self, doc):
        doc = dict(doc)
        doc["_id"] = str(self.auto_id)
        self.auto_id += 1
        self.data.append(doc)
        return type("Result", (), {"inserted_id": doc["_id"]})()

    def find_one(self, filt):
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                return doc
        return None

    def find(self, filt=None):
        if not filt:
            return list(self.data)
        return [doc for doc in self.data if all(doc.get(k) == v for k, v in filt.items())]

    def update_one(self, filt, update):
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                for k, v in update.get("$set", {}).items():
                    doc[k] = v
                return type("Result", (), {"modified_count": 1})()
        return type("Result", (), {"modified_count": 0})()

    def delete_one(self, filt):
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                self.data.remove(doc)
                return type("Result", (), {"deleted_count": 1})()
        return type("Result", (), {"deleted_count": 0})()


class FakeDB:
    def __init__(self):
        self.chats = FakeCollection()
        self.messages = FakeCollection()


db = FakeDB()


# the chat DAL
class chat_dal:
    @staticmethod
    def insert_one_chat(data):
        return db.chats.insert_one(data).inserted_id

    @staticmethod
    def find_one_chat(filt):
        return db.chats.find_one(filt)

    @staticmethod
    def find_all_chats():
        return db.chats.find()

    @staticmethod
    def update_one_chat(filt, data):
        return db.chats.update_one(filt, {"$set": data}).modified_count > 0

    @staticmethod
    def delete_one_chat(filt):
        return db.chats.delete_one(filt).deleted_count > 0


# the messages DAL
class messages_dal:
    @staticmethod
    def insert_one_message(data):
        return db.messages.insert_one(data).inserted_id

    @staticmethod
    def find_one_message(filt):
        return db.messages.find_one(filt)

    @staticmethod
    def find_all_messages():
        return db.messages.find()

    @staticmethod
    def update_one_message(filt, data):
        return db.messages.update_one(filt, {"$set": data}).modified_count > 0

    @staticmethod
    def delete_one_message(filt):
        return db.messages.delete_one(filt).deleted_count > 0
