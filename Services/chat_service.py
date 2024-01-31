from flask import jsonify
from Database.firebase import Firebase

class ChatService:
    def __init__(self, db) -> None:
        self.db = db
    
    def create_chat(self, user_id):
        try:
            doc_ref = self.db.collection('chat').doc(user_id)
            doc_ref.set({
                "messages":{}
            })
            return jsonify({"message": "chat created successfully", "error": False}), 201

        except Exception as e:
            return jsonify({"message": "Error creating the chat", "error": True}), 400
    
    def add_queries(self, user_id, chat_id, role, content):
        try:
            doc_ref = self.db.collection('chat').doc(user_id)
            
            doc_ref.update({"messages": {
                chat_id: [{"role": role, "content": content}]
            }})
            return jsonify({"message": "history stored", "error": False}), 201
        except Exception as e:
            return jsonify({"message": "Error occured while storing the chat", "error": True}), 400