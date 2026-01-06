import re, os, tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def clean_text(text):
    text = re.sub(r'[*#`]', '', text)
    return re.sub(r'\n\s*\n', '\n\n', text).strip()

def process_pdf(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(file_bytes)
        path = f.name

    try:
        docs = PyPDFLoader(path).load()
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(docs)

        return FAISS.from_documents(
            chunks,
            GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        )
    finally:
        os.remove(path)
