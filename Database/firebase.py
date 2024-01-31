import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import os


class Firebase:
    def __init__(self) -> None:
        path = os.path.abspath(os.path.dirname(__file__)) + "/credentials.json"
        self.credentials = credentials.Certificate(path)
        firebase_admin.initialize_app(self.credentials, {"databaseURL": "https://personalizegpt-default-rtdb.asia-southeast1.firebasedatabase.app/"})
        
        self.db = firestore.client()
        sys.modules[__name__] = self.db

    def dbRef(self):
        return self.db

    def create_user(self, doc_name):
        docRef = self.db.collection("users").document(doc_name)
        return docRef