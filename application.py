from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os

from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate

# import firebase class
from Database.firebase import Firebase
# importing Controllers
from Controllers.user_controllers import UserControllers
from Controllers.chat_controllers import ChatControllers
from chatbots.retrieval import create_chain
# password_utils
from utils.password_utils import hash_password
from utils.propmts import chat_with_human, get_greeting

app = Flask(__name__)
CORS(app=app, supports_credentials=True)

# initializing the controllers
db_ref = Firebase().dbRef()
user_controllers = UserControllers(db_ref)
chat_controllers = ChatControllers(db_ref)

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
    choosed_llm = data.get("choosed_llm")
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
      "choosed_llm": choosed_llm,
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
  

@app.route("/get-greetings")
def get_greetings():
  user_id = request.args.get("user_id")
  chain_responses = {}
  try:
    response, status_code = user_controllers.get_user_by_user_id(user_id)
    if status_code == 200:
      chain = create_chain()
      response_json = response.get_json()
      prompt_template = PromptTemplate.from_template(get_greeting())
      prompt = prompt_template.format(
        personality=response_json['first_name'],
        user_description=response_json['first_name'],
        user_name=response_json['first_name']
      )
      chain_responses = {"data": chain.predict(input=prompt), "error": False}
      return jsonify(chain_responses), 200
    else:
      return jsonify({"message": "Error occured while Login", "error": e}), 400
  except Exception as e:
    return jsonify({"message": "Error occured while Login", "error": e}), 400

  
@app.route("/query", methods=["POST"])
def query():
  data = request.get_json()
  user_id = data.get("user_id")
  choosed_llm = data.get("choosed_llm")
  chat_history = data.get('chat_history')
  if data.get("chat_id"):
    chat_id = data.get('chat_id')
  else:
    chat_id = None
  message = data.get('message')
  chain_responses = {}
  try:
    chain = create_chain()
    response, status_code = user_controllers.get_user_by_user_id(user_id)
    if status_code == 200:
      prompt_template = PromptTemplate.from_template(chat_with_human())
      response_json = response.get_json()
      prompt = prompt_template.format(
        input=message,
        personality=response_json['first_name'],
        user_description=response_json['first_name'],
        user_name=response_json['first_name']
      )
      chain_responses = {"data": chain.predict(input=prompt), "error": False}
      return jsonify(chain_responses), 200
      
    else:
      return jsonify({"message": "Error occured while Fetching", "error": True}), 400

  except Exception as e:
    return jsonify({"message": "Error occured while Fetching", "error": True}), 400


if __name__ == "__main__":
  load_dotenv(find_dotenv(), override=True);
  app.run(debug=True)