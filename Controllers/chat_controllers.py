from flask import jsonify
from Services.chat_service import ChatService

class ChatControllers:
    def __init__(self, db) -> None:
        self.db = db
        self.messages = []
        self.chat_service = ChatService(self.db)
    
    def chat_with_bot(self, user_id, role, content, chat_id = None):
        if chat_id:
            return self.chat_service.add_queries(user_id, chat_id, role, content)
        else:
            return self.chat_service.create_chat(user_id)
