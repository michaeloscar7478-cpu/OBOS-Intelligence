import chromadb
from chromadb.config import Settings
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize ChromaDB
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chromadb_store"))

collection = client.get_or_create_collection(
    name="obos_documents",
    metadata={"hnsw:space": "cosine"}
)

# Function to add documents
def add_document(text: str, doc_id: str):
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_query(text)

    collection.add(
        ids=[doc_id],
        embeddings=[vector],
        documents=[text]
    )

# Function to search documents
def search(query: str, n_results=3):
    embeddings = OpenAIEmbeddings()
    query_vector = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )

    return results
