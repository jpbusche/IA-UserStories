from langchain_community.document_loaders import PyPDFLoader, TextLoader, \
    UnstructuredHTMLLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from src.settings import MODEL


class Reader:

    EXTENSION_DOCUMENT = {
        "pdf": PyPDFLoader,
        "txt": TextLoader,
        "html": UnstructuredHTMLLoader,
        "md": UnstructuredMarkdownLoader
    }

    def __init__(self, path):
        self.path = path

    def load_document(self):
        extension = self.path.split(".")[-1]
        loader = self.EXTENSION_DOCUMENT[extension](self.path)
        return loader.load()
    
    def retrieve_document(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
        documents = text_splitter.split_documents(self.load_document())
        vector = Chroma.from_documents(documents=documents, embedding=OllamaEmbeddings(model=MODEL))
        return vector.as_retriever()
    
    def format_documents(self, documents):
        return "\n\n".join(document.page_content for document in documents)
    
    def get_context(self, question):
        retriever = self.retrieve_document()
        documents = retriever.invoke(question)
        return self.format_documents(documents)
    