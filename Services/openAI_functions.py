from openai import OpenAI
from langchain_openai import ChatOpenAI

class OpenAIService:
  def __init__(self, db):
    self.db = db
    self.llm = ChatOpenAI()
  
  # def generateChat(self, query, message=None):

  
