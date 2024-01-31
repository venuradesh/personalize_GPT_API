from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os

# import firebase class
from Database.firebase import Firebase
# importing userControls
from Controllers.user_controllers import UserControllers
# password_utils
from utils.password_utils import hash_password

app = Flask(__name__)
CORS(app=app, supports_credentials=True)

# creating the user controllers
user_controllers = UserControllers(Firebase().dbRef())

app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
app.config['LLAMA_API_KEY'] = os.environ.get("LLAMA_API_KEY")

@app.route("/signup", methods=["POST"])
def create_character():
  data = request.get_json()
  try:
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    designation = data.get("designation")
    organization_name = data.get("organization_name")
    email = data.get("email")
    description = data.get("description")
    personality = data.get("personality")
    password = hash_password(data.get("password"))
    if data.get("openai_api_key"):
      openai_api_key = data.get("openai_api_key")
      os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
      openai_api_key = None

    response,status_code = user_controllers.user_create({
      "first_name": first_name, 
      "last_name": last_name, 
      "date_of_birth": date_of_birth, 
      "designation": designation,
      "organization_name": organization_name,
      "email": email,
      "description": description,
      "personality": personality,
      "password": password,
      "openai_api_key": openai_api_key
    })
    return response, status_code
  except Exception as e:
    return jsonify({"message": "Error occured while creating the user", "error": e}), 400
  
@app.route("/login", methods=["POST"])
def login():
  data = request.get_json()
  try:
    email = data.get('email')
    password = data.get('password')
    response, status_code = user_controllers.login_user(email, password)
    return response, status_code
  except Exception as e:
    return jsonify({"message": "Error occured while Login", "error": e}), 400

if __name__ == "__main__":
  load_dotenv(find_dotenv(), override=True);
  app.run(debug=True)