import gradio as gr
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import pdf
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings


def load_pdf_document(pdf_file_path):
    loader = pdf.PyPDFLoader(pdf_file_path)
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    document_splits = text_splitter.split_documents(document)
    embeddings = OllamaEmbeddings(model="llama3.1")
    vector_store = Chroma.from_documents(documents=document_splits, embedding=embeddings)
    return vector_store.as_retriever()

def format_documents(documents):
    return "\n\n".join(document.page_content for document in documents)

def rag_chain(pdf_file_path, question):
    retriever = load_pdf_document(pdf_file_path)
    retrieved_documents = retriever.invoke(question)
    formattted_context = format_documents(retrieved_documents)
    formatted_prompt = f"Question: {question}\n\nContext: {formattted_context}"
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": formatted_prompt}])
    return response['message']['content']