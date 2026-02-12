"""
Application entry point.

Run this file to start the RAG system.
"""

from langchain.schema import Document
from app.retriever import build_vector_store
from app.graph import build_graph
import os


def load_sample_docs():
    with open("data/sample_docs.txt", "r") as f:
        text = f.read()

    return [Document(page_content=text)]


if __name__ == "__main__":
    # Build vector store if not exists
    if not os.path.exists("./chroma_db"):
        docs = load_sample_docs()
        build_vector_store(docs)

    app = build_graph()

    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.lower() == "exit":
            break

        result = app.invoke({"question": question})
        print("\nAnswer:\n", result["generation"])
