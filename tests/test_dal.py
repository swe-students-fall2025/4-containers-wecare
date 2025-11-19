from backend.DAL import chat_dal, messages_dal

#testcases for DAL
def test_chat_insert_one():
    chat_id = chat_dal.insert_one_chat({"user": "amy"})
    assert chat_id != ""

def test_chat_find_one():
    chat_dal.insert_one_chat({"user": "amy"})
    result = chat_dal.find_one_chat({"user": "amy"})
    assert result["user"] == "amy"

def test_chat_find_all():
    chat_dal.insert_one_chat({"a": 1})
    chat_dal.insert_one_chat({"b": 2})
    assert len(chat_dal.find_all_chats()) == 2

def test_chat_update_one():
    chat_dal.insert_one_chat({"id": 1})
    assert chat_dal.update_one_chat({"id": 1}, {"mood": "happy"}) is True

def test_chat_delete_one():
    chat_dal.insert_one_chat({"id": 9})
    assert chat_dal.delete_one_chat({"id": 9}) is True


# Messages DAL

def test_msg_insert_one():
    msg_id = messages_dal.insert_one_message({"text": "hi"})
    assert msg_id != ""

def test_msg_find_one():
    messages_dal.insert_one_message({"sender": "bot"})
    result = messages_dal.find_one_message({"sender": "bot"})
    assert result["sender"] == "bot"

def test_msg_find_all():
    messages_dal.insert_one_message({"a": 1})
    messages_dal.insert_one_message({"a": 2})
    assert len(messages_dal.find_all_messages()) == 2

def test_msg_update_one():
    messages_dal.insert_one_message({"id": 2})
    assert messages_dal.update_one_message({"id": 2}, {"ok": True}) is True

def test_msg_delete_one():
    messages_dal.insert_one_message({"id": 5})
    assert messages_dal.delete_one_message({"id": 5}) is True
