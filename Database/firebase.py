import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

credentials = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(credentials, {"databaseURL": "https://personalizegpt-default-rtdb.asia-southeast1.firebasedatabase.app/"})

db = firestore.client()

sys.modules[__name__] = db