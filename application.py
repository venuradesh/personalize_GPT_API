from flask import Flask, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app=app, supports_credentials=True)

app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

@app.route("/user-query", methods=["POST"])
def user_query():
  data = request.get_json()
  user_id = data.get("user_id")
  query = data.get("query")


if __name__ == "__main__":
  load_dotenv();
  app.run(debug=True)