# main.py code and logic explanations

---

## ✅ Fully Commented Version of code

```python
"""
Application entry point.

This file acts as the CLI interface for the RAG system.
When executed directly, it:

1. Ensures a vector store exists
2. Builds the LangGraph workflow
3. Accepts user input in a loop
4. Invokes the graph
5. Prints the generated answer
"""

# LangChain Document abstraction used for storing text data
from langchain.schema import Document

# Function responsible for building and persisting the vector store
from app.retriever import build_vector_store

# Function that constructs and compiles the LangGraph workflow
from app.graph import build_graph

# Standard Python library for filesystem checks
import os


def load_sample_docs():
    """
    Loads sample documents from a text file and converts them
    into LangChain Document objects.

    Why wrap in Document?
    ----------------------
    LangChain's vector stores expect a list of Document objects,
    not raw strings. Document objects allow metadata attachment
    and standardize downstream processing.

    Returns:
        List[Document]: List containing a single document built
        from the contents of sample_docs.txt
    """

    # Open the sample document file in read mode
    with open("data/sample_docs.txt", "r") as f:
        text = f.read()

    # Wrap raw text inside a LangChain Document object
    return [Document(page_content=text)]


# This condition ensures the code runs only when the file
# is executed directly (not when imported as a module)
if __name__ == "__main__":

    # ---------------------------------------------------------
    # Step 1: Ensure Vector Store Exists
    # ---------------------------------------------------------

    # Check if Chroma persistence directory exists
    # This prevents rebuilding embeddings every time the app runs
    if not os.path.exists("./chroma_db"):

        # Load sample documents from file
        docs = load_sample_docs()

        # Build and persist the vector store
        # This:
        #   - Generates embeddings
        #   - Stores them in Chroma
        #   - Saves them to disk
        build_vector_store(docs)

    # ---------------------------------------------------------
    # Step 2: Build LangGraph Workflow
    # ---------------------------------------------------------

    # Construct the stateful RAG workflow
    # This compiles:
    #   Retrieve node
    #   Grade node
    #   Conditional routing
    #   Generate/Fallback nodes
    app = build_graph()

    # ---------------------------------------------------------
    # Step 3: Interactive CLI Loop
    # ---------------------------------------------------------

    while True:
        # Ask user for a question
        question = input("\nAsk a question (or type 'exit'): ")

        # Allow graceful exit
        if question.lower() == "exit":
            break

        # -----------------------------------------------------
        # Step 4: Invoke LangGraph Workflow
        # -----------------------------------------------------

        # The graph expects a dictionary matching RAGState
        # Here we initialize state with only the question.
        # Other fields will be filled by nodes.
        result = app.invoke({"question": question})

        # -----------------------------------------------------
        # Step 5: Print Final Output
        # -----------------------------------------------------

        # The graph returns the final state dictionary.
        # We extract the generated answer from it.
        print("\nAnswer:\n", result["generation"])
```

---

# 🔎 What’s Really Happening Architecturally

Let’s break it down at a systems level.

---

## 1️⃣ Why `if __name__ == "__main__"`?

This ensures:

* If you run:

  ```
  python -m app.main
  ```

  → the CLI runs.

* If another file imports this module:

  ```python
  import app.main
  ```

  → the CLI does NOT auto-run.

This is standard Python best practice.

---

## 2️⃣ Why Check for `./chroma_db`?

```python
if not os.path.exists("./chroma_db"):
```

Vector embedding creation is expensive.

We only want to build it once.

Without this check:

* Every run would re-embed documents.
* Slower startup.
* More API cost.

This is a persistence optimization.

---

## 3️⃣ What Does `build_vector_store()` Actually Do?

It:

1. Generates embeddings using OpenAI
2. Stores them in Chroma
3. Persists them locally to disk

So subsequent runs can load from disk instead of recomputing.

---

## 4️⃣ What Does `build_graph()` Do?

It compiles:

```
Retrieve → Grade → Conditional → Generate/Fallback
```

into a runnable state machine.

When you call:

```python
app.invoke({"question": question})
```

LangGraph:

1. Initializes state
2. Executes retrieve node
3. Executes grade node
4. Follows conditional edge
5. Executes final node
6. Returns full state

---

## 5️⃣ What Is `result`?

It’s the final state dictionary.

Something like:

```python
{
    "question": "...",
    "retrieved_docs": [...],
    "is_relevant": True,
    "generation": "Final answer..."
}
```

You extract:

```python
result["generation"]
```

---

# 🧠 Important Design Observations

### ✅ Good Things About This Design

* Clean separation of concerns
* Persistent embeddings
* Modular architecture
* Graph-based orchestration
* Safe CLI entry

---

### ⚠️ Things to Improve for Production

If this were production-grade:

* Add logging
* Add try/except around `app.invoke`
* Add input validation
* Add timeout handling
* Add rate limit handling
* Add graceful shutdown
* Add structured logs
* Add environment-based path config

---

# 🔥 Why This Is Architecturally Clean

Notice:

`main.py` does NOT:

* Contain retrieval logic
* Contain LLM logic
* Contain grading logic
* Contain graph wiring

It only orchestrates at the top level.

That’s clean architecture.

---

# 📌 Final Mental Model

This file is:

> The thin interface layer between user and graph engine.

Everything complex happens inside modular components.
