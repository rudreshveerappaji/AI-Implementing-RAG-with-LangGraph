
# ✅ Fully Commented `graph.py`

```python
"""
LangGraph workflow definition.

This file defines the entire RAG workflow using LangGraph.

Flow:
1. Retrieve documents
2. Grade relevance
3. If relevant → Generate answer
4. If not → Fallback response

This is the orchestration layer of the system.
It connects independent components into a stateful graph.
"""

# Core LangGraph classes
# - StateGraph: Used to define a graph with state transitions
# - END: Special marker indicating workflow termination
from langgraph.graph import StateGraph, END

# TypedDict defining shared state structure across nodes
from app.state import RAGState

# Import modular components (business logic separated cleanly)
from app.retriever import load_vector_store, retrieve_documents
from app.generator import generate_answer
from app.grader import grade_relevance


# -------------------------------------------------------------
# Global Vector Store Initialization
# -------------------------------------------------------------

# Load persisted vector store once at module import time.
# This avoids reloading embeddings on every request.
# In production, you might lazy-load or inject this.
vectorstore = load_vector_store()


# -------------------------------------------------------------
# Node 1: Retrieve
# -------------------------------------------------------------

def retrieve(state: RAGState):
    """
    Retrieve relevant documents from vector store.

    Input:
        state["question"]

    Output:
        Updates state with:
            {"retrieved_docs": docs}

    Important:
    - Nodes receive entire state
    - Nodes return partial updates
    - LangGraph merges updates into global state
    """

    docs = retrieve_documents(vectorstore, state["question"])

    # Return partial state update
    return {"retrieved_docs": docs}


# -------------------------------------------------------------
# Node 2: Grade
# -------------------------------------------------------------

def grade(state: RAGState):
    """
    Evaluate whether retrieved documents are relevant
    to the user’s question.

    Input:
        state["question"]
        state["retrieved_docs"]

    Output:
        {"is_relevant": True/False}

    This enables conditional routing.
    """

    is_relevant = grade_relevance(
        state["question"],
        state["retrieved_docs"]
    )

    return {"is_relevant": is_relevant}


# -------------------------------------------------------------
# Node 3: Generate
# -------------------------------------------------------------

def generate(state: RAGState):
    """
    Generate final answer using retrieved documents.

    Input:
        state["question"]
        state["retrieved_docs"]

    Output:
        {"generation": answer}
    """

    answer = generate_answer(
        state["question"],
        state["retrieved_docs"]
    )

    return {"generation": answer}


# -------------------------------------------------------------
# Node 4: Fallback
# -------------------------------------------------------------

def fallback(state: RAGState):
    """
    Return fallback response if documents are not relevant.

    This prevents hallucinated answers.
    """

    return {
        "generation": "Sorry, I couldn't find relevant information."
    }


# -------------------------------------------------------------
# Graph Builder
# -------------------------------------------------------------

def build_graph():
    """
    Construct and compile the LangGraph workflow.

    Steps:
    1. Initialize StateGraph with state schema
    2. Add nodes
    3. Define edges
    4. Define conditional routing
    5. Compile into executable app
    """

    # Initialize graph with typed state
    workflow = StateGraph(RAGState)

    # -------------------------------
    # Add Nodes
    # -------------------------------

    # Each node has:
    #   - Unique name
    #   - Function that modifies state
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade)
    workflow.add_node("generate", generate)
    workflow.add_node("fallback", fallback)

    # -------------------------------
    # Define Graph Flow
    # -------------------------------

    # Entry point of workflow
    workflow.set_entry_point("retrieve")

    # Linear edge: retrieve → grade
    workflow.add_edge("retrieve", "grade")

    # -------------------------------
    # Conditional Routing
    # -------------------------------

    workflow.add_conditional_edges(
        "grade",

        # Decision function
        # Reads state and determines next node
        lambda state: "generate" if state["is_relevant"] else "fallback",

        # Mapping of return values → node names
        {
            "generate": "generate",
            "fallback": "fallback",
        },
    )

    # -------------------------------
    # Termination
    # -------------------------------

    # After generate → END
    workflow.add_edge("generate", END)

    # After fallback → END
    workflow.add_edge("fallback", END)

    # Compile graph into executable object
    return workflow.compile()
```

---

# 🧠 How LangGraph Actually Works Internally

When you call:

```python
app.invoke({"question": question})
```

LangGraph:

1. Initializes state:

   ```
   {
       "question": "...",
       "retrieved_docs": None,
       "is_relevant": None,
       "generation": None
   }
   ```

2. Executes entry node (`retrieve`)

3. Merges returned state

4. Follows defined edges

5. Executes `grade`

6. Runs conditional routing

7. Executes chosen node

8. Hits END

9. Returns final state

It behaves like a deterministic state machine.

---

# 🔎 Important Design Concepts

## 1️⃣ State Is Central

Every node:

* Receives full state
* Returns partial state update

LangGraph merges updates automatically.

This is functional programming style.

---

## 2️⃣ Nodes Are Pure Functions

Each node:

* Has no side effects (ideally)
* Takes state
* Returns new state fields

This makes debugging easy.

---

## 3️⃣ Conditional Edges Are The Real Power

This line:

```python
workflow.add_conditional_edges(...)
```

Is what turns a pipeline into a workflow.

Without this, it would just be:

```
retrieve → grade → generate
```

Now it becomes:

```
retrieve → grade → (generate OR fallback)
```

---

# 🔥 Architectural Strength

This file:

* Contains zero business logic
* Only wires components together
* Is purely orchestration

That’s clean separation of concerns.

---

# ⚠️ Production Considerations

### 1️⃣ Global Vectorstore

```python
vectorstore = load_vector_store()
```

This loads at import time.

Better production pattern:

* Inject dependencies
* Use dependency container
* Lazy-load

---

### 2️⃣ No Error Handling

If grading fails:

* Graph will crash.

Production:

* Wrap nodes with try/except
* Add retry logic

---

### 3️⃣ No Observability

In enterprise:

* Add logging per node
* Add tracing
* Add execution timing

---

# 📌 Mental Model

Think of this file as:

> The conductor of an orchestra.

It doesn’t play instruments.
It tells:

* Retriever → Play
* Grader → Decide
* Generator → Respond

---

# 🚀 What Makes This Senior-Level Design?

* Stateful workflow
* Clear node isolation
* Conditional routing
* Extensible architecture
* Clean orchestration layer

---
