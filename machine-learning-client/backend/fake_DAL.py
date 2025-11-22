"""
A fake Data Access Layer (DAL) to simulate MongoDB operations for testing purposes.
"""


''' 
fake database to simulate MongoDB operations for testing
'''
class fake_collection:
    """test with fake collections"""

    def __init__(self):
        """
        Initialize an empty collection.
        """
        self.data = []
        self.auto_id = 1

    def insert_one(self, doc):
        """
        Insert a document into the collection.
        """
        doc = dict(doc)
        doc["_id"] = str(self.auto_id)
        self.auto_id += 1
        self.data.append(doc)
        return type("Result", (), {"inserted_id": doc["_id"]})()

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
        if not filt:
            return list(self.data)
        return [
            doc for doc in self.data if all(doc.get(k) == v for k, v in filt.items())
        ]

    def update_one(self, filt, update):
        """
        update one document matching the filter.
        """
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                for k, v in update.get("$set", {}).items():
                    doc[k] = v
                return type("Result", (), {"modified_count": 1})()
        return type("Result", (), {"modified_count": 0})()

    def delete_one(self, filt):
        """
        delete one document matching the filter.
        """
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filt.items()):
                self.data.remove(doc)
                return type("Result", (), {"deleted_count": 1})()
        return type("Result", (), {"deleted_count": 0})()

'''
class fake_db
'''
class fake_db:
    def __init__(self):
        """
        Initialize the fake database with chats and messages collections.
        """
        self.chats = fake_collection()
        self.messages = fake_collection()


db = fake_db()


'''
The chats DAL
'''
class chat_dal:
    @staticmethod
    def insert_one_chat(data):
        """
        insert one chat document.
        """
        return db.chats.insert_one(data).inserted_id

    @staticmethod
    def find_one_chat(filt):
        """
        find one chat document matching the filter.
        """
        return db.chats.find_one(filt)

    @staticmethod
    def find_all_chats():
        """
        find all chat documents.
        """
        return db.chats.find()

    @staticmethod
    def update_one_chat(filt, data):
        """
        update one chat document matching the filter.
        """
        return db.chats.update_one(filt, {"$set": data}).modified_count > 0

    @staticmethod
    def delete_one_chat(filt):
        """
        delete one chat document matching the filter.
        """
        return db.chats.delete_one(filt).deleted_count > 0


'''
class messages_dal
'''
class messages_dal:
    @staticmethod
    def insert_one_message(data):
        """
        insert one message document.
        """
        return db.messages.insert_one(data).inserted_id

    @staticmethod
    def find_one_message(filt):
        """
        find one message document matching the filter.
        """
        return db.messages.find_one(filt)

    @staticmethod
    def find_all_messages():
        """
        find all message documents.
        """
        return db.messages.find()

    @staticmethod
    def update_one_message(filt, data):
        """
        update one message document matching the filter.
        """
        return db.messages.update_one(filt, {"$set": data}).modified_count > 0

    @staticmethod
    def delete_one_message(filt):
        """
        ddelete one message document matching the filter.
        """
        return db.messages.delete_one(filt).deleted_count > 0
