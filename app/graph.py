"""
LangGraph workflow definition.

Flow:
1. Retrieve documents
2. Grade relevance
3. If relevant → Generate answer
4. If not → End with fallback
"""

from langgraph.graph import StateGraph, END
from app.state import RAGState
from app.retriever import load_vector_store, retrieve_documents
from app.generator import generate_answer
from app.grader import grade_relevance


vectorstore = load_vector_store()


def retrieve(state: RAGState):
    docs = retrieve_documents(vectorstore, state["question"])
    return {"retrieved_docs": docs}


def grade(state: RAGState):
    is_relevant = grade_relevance(state["question"], state["retrieved_docs"])
    return {"is_relevant": is_relevant}


def generate(state: RAGState):
    answer = generate_answer(state["question"], state["retrieved_docs"])
    return {"generation": answer}


def fallback(state: RAGState):
    return {"generation": "Sorry, I couldn't find relevant information."}


def build_graph():
    workflow = StateGraph(RAGState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade)
    workflow.add_node("generate", generate)
    workflow.add_node("fallback", fallback)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade")

    workflow.add_conditional_edges(
        "grade",
        lambda state: "generate" if state["is_relevant"] else "fallback",
        {
            "generate": "generate",
            "fallback": "fallback",
        },
    )

    workflow.add_edge("generate", END)
    workflow.add_edge("fallback", END)

    return workflow.compile()
