import os
import certifi
import truststore

truststore.inject_into_ssl()
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def ingest_pdf():
    if not PDF_PATH:
        raise ValueError("PDF_PATH não configurado no .env")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não configurado no .env")
    if not COLLECTION_NAME:
        raise ValueError("PG_VECTOR_COLLECTION_NAME não configurado no .env")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não configurado no .env")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
    )

    vector_store.add_documents(chunks)
    print(f"Ingestão concluída com sucesso. Total de chunks: {len(chunks)}")


if __name__ == "__main__":
    ingest_pdf()