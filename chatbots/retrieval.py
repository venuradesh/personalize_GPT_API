import os
from langchain.chains import ConversationChain
from llamaapi import LlamaAPI
# from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI, OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import create_tagging_chain
from langchain_experimental.llms import ChatLlamaAPI


def create_chain():
    # conv_memory = ConversationBufferMemory()
    
    GPT = ChatOpenAI(model_name="gpt-3.5-turbo")
    chatbot = ConversationChain(
        llm=GPT,
        verbose=True,
        memory=ConversationBufferMemory()
    )
    return chatbot

# def llm_chain(prompt_template):
#     GPT = ChatOpenAI(model_name="gpt-3.5-turbo")
#     llm_chain = LLMChain(
#         llm = GPT,
#         prompt = prompt_template
#     )
#     return llm_chain

# def conversational_chain(vector_store):
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo")
#     memory = ConversationBufferMemory(
#         memory_key="doc-chat-history", return_messages=True
#     )
#     # conversational_chain = Conversational
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         memory=memory,
#         retriever=vector_store.as_retriever()
#     )
#     return conversation_chain

# def load_qa_chain():
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo")
#     chain = load_qa_chain(llm=llm, chain_type='stuff')
#     return chain

def retrieval_chain(retriever):
    llm = OpenAI(temperature=0.3)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    return qa

# def llama_chain():
#     llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
#     model = ChatLlamaAPI(client=llama)
#     schema = {
#         "properties": {
#             "sentiment": {
#                 "type": "string",
#                 "description": "positive",
#             },
#             "aggressiveness": {
#                 "type": "integer",
#                 "description": "4",
#             },
#             "language": {"type": "string", "description": "English"},
#         }
#     }
#     chain = create_tagging_chain(schema, model)
#     return chain

def llama_chain():
    llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
    model = ChatLlamaAPI(client=llama)

    chatbot = ConversationChain(
        llm=model,
        verbose=True,
        memory=ConversationBufferMemory()
    )
    return chatbot