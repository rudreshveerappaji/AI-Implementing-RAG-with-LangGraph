"""
Defines the shared state used across the LangGraph workflow.

LangGraph works with a state dictionary. We use TypedDict
for type safety and clarity.
"""

from typing import List, TypedDict
from langchain.schema import Document


class RAGState(TypedDict):
    question: str
    retrieved_docs: List[Document]
    generation: str
    is_relevant: bool
