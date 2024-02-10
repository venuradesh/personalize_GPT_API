from flask import jsonify
from utils.password_utils import validate_password


class UserService:
    def __init__(self, db) -> None:
        self.db = db
    
    def create_user(self, user_data):
        try:
            docRef = self.db.collection("users").document()
            docRef.set(user_data)
            return jsonify({"message": "successfully created"}), 201
        except Exception as e:
            return jsonify({"message": "error in creating the user"}), 400
        
    def login_user(self, email, password):
        try:
            user_docs = self.db.collection("users").stream()
            for doc in user_docs:
                emailRetrived = doc.get('email')
                if(emailRetrived == email):
                    res = validate_password(doc.get('password'), password)
                    if(res): 
                        return jsonify({"message": "user login successful", "error": False, "user_id": doc.id, "first_name": doc.get('first_name'), "last_name": doc.get('last_name'), "choosed_llm": doc.get('choosed_llm')}), 200
                    else: 
                        return jsonify({"message": "incorrect password.", "error": True}),400
                    
            return jsonify({"message": "no user found with the email", "error": True}), 400

        except Exception as e:
            return jsonify({"message": "error occured while login"}), 400
        
    def get_user_details_by_id(self, user_id):
        try:
            user_docs = self.db.collection("users").stream()
            for doc in user_docs:
                return jsonify({
                    "first_name": doc.get('first_name'), 
                    'last_name': doc.get('last_name'),
                    'description': doc.get('description'), 
                    'personality': doc.get('personality'),
                    'designation': doc.get('designation'),  
                    'choosed_llm': doc.get('choosed_llm')
                }), 200
        except:
            return jsonify({"message": "error occured while fetching data"}), 400