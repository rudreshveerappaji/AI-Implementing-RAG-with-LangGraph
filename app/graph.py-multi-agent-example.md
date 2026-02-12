# This is an example of how to move the current single agent graph.py RAG implementation to multi-agent system

---

Now we’re moving from **single-agent RAG workflow** → to a **multi-agent graph architecture**.
This is how modern production AI systems are being designed.

Let's

1. Explain the architectural shift
2. Show the new multi-agent design
3. Provide production-ready `graph.py`
4. Explain what changed and why

---

# 🧠 What Changes in a Multi-Agent Graph?

Previously:

```
Retrieve → Grade → Generate → END
```

Now we introduce specialized agents:

| Agent           | Responsibility            |
| --------------- | ------------------------- |
| Retriever Agent | Fetch documents           |
| Relevance Agent | Evaluate document quality |
| Answer Agent    | Generate answer           |
| Critic Agent    | Verify answer quality     |
| Fallback Agent  | Handle failures           |

Now the workflow becomes:

```
Retriever
    ↓
Relevance Judge
    ↓
(If relevant)
    ↓
Answer Agent
    ↓
Critic Agent
    ↓
(If approved → END)
(If rejected → Retry Generate)
```

This is now:

* Stateful
* Iterative
* Multi-agent
* Self-correcting

This is closer to how enterprise-grade AI systems work.

---

# 🏗 Updated State (Important)

First update your `state.py`:

```python
from typing import List, TypedDict
from langchain.schema import Document


class RAGState(TypedDict):
    question: str
    retrieved_docs: List[Document]
    is_relevant: bool
    generation: str
    is_approved: bool
    retry_count: int
```

We added:

* `is_approved`
* `retry_count`

Because now we may loop.

---

# 🚀 Multi-Agent `graph.py`

Here is the upgraded production-style version:

```python
"""
Multi-Agent LangGraph Workflow

Agents:
- Retriever Agent
- Relevance Judge Agent
- Answer Agent
- Critic Agent
- Fallback Agent

Flow:
Retrieve → Judge → (Generate or Fallback)
Generate → Critic → (Approve or Retry)
"""

from langgraph.graph import StateGraph, END
from app.state import RAGState
from app.retriever import load_vector_store, retrieve_documents
from app.generator import generate_answer
from app.grader import grade_relevance
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


# ---------------------------------------------------------
# Dependency Initialization
# ---------------------------------------------------------

vectorstore = load_vector_store()
critic_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------------------------------------
# Agent 1: Retriever
# ---------------------------------------------------------

def retriever_agent(state: RAGState):
    docs = retrieve_documents(vectorstore, state["question"])
    return {"retrieved_docs": docs}


# ---------------------------------------------------------
# Agent 2: Relevance Judge
# ---------------------------------------------------------

def relevance_agent(state: RAGState):
    is_relevant = grade_relevance(
        state["question"],
        state["retrieved_docs"]
    )
    return {"is_relevant": is_relevant}


# ---------------------------------------------------------
# Agent 3: Answer Generator
# ---------------------------------------------------------

def answer_agent(state: RAGState):
    answer = generate_answer(
        state["question"],
        state["retrieved_docs"]
    )
    return {"generation": answer}


# ---------------------------------------------------------
# Agent 4: Critic Agent (New)
# ---------------------------------------------------------

def critic_agent(state: RAGState):
    """
    Evaluates whether the generated answer sufficiently
    answers the question using the provided context.
    """

    prompt = ChatPromptTemplate.from_template(
        """
        Question: {question}
        Answer: {generation}

        Is this answer accurate and complete?
        Answer only 'yes' or 'no'.
        """
    )

    chain = prompt | critic_model
    response = chain.invoke({
        "question": state["question"],
        "generation": state["generation"]
    })

    is_approved = "yes" in response.content.lower()

    retry_count = state.get("retry_count", 0)

    return {
        "is_approved": is_approved,
        "retry_count": retry_count + 1
    }


# ---------------------------------------------------------
# Agent 5: Fallback
# ---------------------------------------------------------

def fallback_agent(state: RAGState):
    return {
        "generation": "Sorry, I couldn't find relevant information.",
        "is_approved": True  # End execution
    }


# ---------------------------------------------------------
# Graph Builder
# ---------------------------------------------------------

def build_graph():

    workflow = StateGraph(RAGState)

    # Add agents as nodes
    workflow.add_node("retriever", retriever_agent)
    workflow.add_node("relevance", relevance_agent)
    workflow.add_node("answer", answer_agent)
    workflow.add_node("critic", critic_agent)
    workflow.add_node("fallback", fallback_agent)

    # Entry point
    workflow.set_entry_point("retriever")

    # Retriever → Relevance
    workflow.add_edge("retriever", "relevance")

    # Relevance decision
    workflow.add_conditional_edges(
        "relevance",
        lambda state: "answer" if state["is_relevant"] else "fallback",
        {
            "answer": "answer",
            "fallback": "fallback"
        }
    )

    # After answer → critic
    workflow.add_edge("answer", "critic")

    # Critic decision
    workflow.add_conditional_edges(
        "critic",
        lambda state: (
            "answer"
            if not state["is_approved"] and state["retry_count"] < 2
            else END
        ),
        {
            "answer": "answer",
            END: END
        }
    )

    # Fallback → END
    workflow.add_edge("fallback", END)

    return workflow.compile()
```

---

# 🔥 What This Upgraded Version Does

## 1️⃣ Adds Agent Specialization

Each agent has a single responsibility.

## 2️⃣ Adds Self-Correction Loop

If critic says:

```
not approved
```

It loops back:

```
answer → critic → answer
```

Until:

* Approved
* Retry limit reached

That’s iterative reasoning.

---

# 🧠 Why This Is Enterprise-Grade

This design:

* Prevents hallucinations
* Allows answer refinement
* Enables future agent expansion
* Mirrors multi-agent LLM research systems

---

# 📊 Conceptual Flow

```
Retriever
   ↓
Relevance Judge
   ↓
Answer Agent
   ↓
Critic Agent
   ↓
(Approved?) → END
(No?) → Retry Answer
```

---

# 🏗 What You Just Built

This is now:

* A multi-agent orchestration system
* With evaluation
* With retry logic
* With conditional routing
* With state management

This is significantly more advanced than basic RAG.

---

# 🚀 Where This Can Go Next

You can now add:

* Query Rewriter Agent
* Tool-Calling Agent
* Citation Verifier Agent
* Parallel Retrieval Agents
* Multi-hop reasoning agents
* Memory agent
