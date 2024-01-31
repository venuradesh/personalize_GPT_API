from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

def create_chain():
    # conv_memory = ConversationBufferMemory()
    
    GPT = ChatOpenAI(model_name="gpt-3.5-turbo")
    chatbot = ConversationChain(
        llm=GPT,
        verbose=True,
    )
    return chatbot

def llm_chain(prompt_template):
    GPT = ChatOpenAI(model_name="gpt-3.5-turbo")
    llm_chain = LLMChain(
        llm = GPT,
        prompt = prompt_template
    )
    return llm_chain