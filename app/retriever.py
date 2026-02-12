"""
Retriever module.

Responsible for:
- Creating embeddings
- Storing documents
- Retrieving relevant documents
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.config import OPENAI_API_KEY, CHROMA_COLLECTION_NAME, PERSIST_DIRECTORY
import os


def build_vector_store(documents: list[Document]) -> Chroma:
    """
    Builds and persists a Chroma vector store.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    vectorstore.persist()
    return vectorstore


def load_vector_store() -> Chroma:
    """
    Loads an existing persisted vector store.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )


def retrieve_documents(vectorstore: Chroma, query: str, k: int = 4):
    """
    Retrieves top-k relevant documents.
    """
    return vectorstore.similarity_search(query, k=k)
