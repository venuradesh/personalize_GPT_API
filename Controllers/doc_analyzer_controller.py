from chatbots.doc_analyzer import DocumentAnalyzer

class DocAnalyzerController:
    def __init__(self):
        self.file = None
        self.document_analyzer = DocumentAnalyzer()
        pass

    def get_text_chunks(self, file):
        self.file = file
        return self.document_analyzer.split_text(file)
    
    def get_vector_store(self, text_chunks):
        return self.document_analyzer.get_vector_store(text_chunks)