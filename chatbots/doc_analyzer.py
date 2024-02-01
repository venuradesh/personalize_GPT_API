from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
# import faiss

class DocumentAnalyzer:
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=0
        )
    
    def split_text(self, file=None):
        whole_text = ""
        loader = PdfReader(file)
        for page in loader.pages:
            whole_text += page.extract_text()
        
        docs = self.text_splitter.split_text(whole_text)
        return docs
    
    def get_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store