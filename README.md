# Implementing RAG with LangGraph

### Implementing RAG with LangGraph with simple, ready to use examples, for educational purposes.

## 📌 Description

This project demonstrates how to implement a **production-ready Retrieval-Augmented Generation (RAG)** system using **LangGraph**.

The examples illustrated in this repository are simple yet powerful and can be used as a strong foundation for building enterprise-grade RAG applications.

This repository is structured with clean architecture, modular components, and production-ready patterns that make it easy to extend and deploy.

---

## 🚀 What This Project Demonstrates

- Graph-based AI workflows using LangGraph
- Stateful multi-step pipelines
- Document retrieval using Chroma vector database
- LLM-powered relevance grading
- Conditional routing in LangGraph
- Modular and maintainable architecture
- Environment-based configuration management

---

## 🧠 Why LangGraph for RAG?

Traditional RAG pipelines can quickly become messy when adding:

- Retrieval steps
- Validation steps
- Query rewriting
- Conditional fallbacks
- Verification stages

LangGraph solves this by allowing you to:

- Explicitly manage application state
- Visually structure your workflow
- Add conditional branching
- Debug each node independently
- Build scalable, maintainable AI systems

---

## 🏗 Architecture Overview

The system follows a structured graph-based workflow:

### Flow:

1. **Retrieve Documents**
2. **Grade Relevance**
3. **Conditional Routing**
   - If relevant → Generate Answer
   - If not relevant → Fallback Response
4. **Return Final Output**

This architecture allows flexible extension such as:

- Adding query rewriting
- Multi-retriever strategies
- Verification nodes
- Self-correction loops
- Tool integrations

---

## 📂 Project Structure

```
implementing-rag-with-langgraph/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── state.py
│   ├── retriever.py
│   ├── generator.py
│   ├── grader.py
│   ├── graph.py
│   └── main.py
│
├── data/
│   └── sample_docs.txt
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Technology Stack

- **LangGraph** – Graph-based AI workflows
- **LangChain** – LLM orchestration
- **OpenAI GPT models** – Text generation & grading
- **ChromaDB** – Vector storage
- **Python 3.9+**
- **python-dotenv** – Environment management

---

## ⚙ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/implementing-rag-with-langgraph.git
cd implementing-rag-with-langgraph
```

---

### 2️⃣ Create a Virtual Environment

**Mac / Linux**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

You can copy from `.env.example`.

---

## ▶ Running the Application

```bash
python -m app.main
```

You will see a CLI prompt:

```
Ask a question (or type 'exit'):
```

Ask questions based on the sample document.

---

## 📄 Example

If your `sample_docs.txt` contains:

```
LangGraph is a framework for building stateful, multi-step AI applications.
```

You can ask:

```
What is LangGraph?
```

The system will:

- Retrieve relevant context
- Grade relevance
- Generate grounded answer
- Return response

---

## 🧩 Core Components Explained

### config.py
Centralized configuration management (API keys, model settings, DB settings).

### state.py
Defines shared application state using TypedDict for type safety.

### retriever.py
Handles:
- Embedding creation
- Vector store persistence
- Similarity search

### grader.py
Uses LLM to evaluate whether retrieved documents are relevant.

### generator.py
Generates grounded answers using retrieved context.

### graph.py
Defines the LangGraph workflow:
- Nodes
- Edges
- Conditional routing
- Entry point

### main.py
CLI entry point for interacting with the RAG system.

---

```
flowchart LR
    User --> LangGraph
    LangGraph --> Retriever
    Retriever --> VectorDB[(Chroma DB)]
    Retriever --> Grader
    Grader -->|Relevant| Generator
    Grader -->|Not Relevant| Fallback
    Generator --> User
    Fallback --> User
```
---

Entry Point

1️⃣ main.py calls:
'''
app.invoke({"question": question})
'''
- This enters the LangGraph workflow.

2️⃣ Retrieve Node (retriever.py)
- Loads Chroma vector store
- Performs similarity search
- Returns top-k relevant documents

3️⃣ Grade Node (grader.py)
- Uses LLM to check:
'''
Are these documents actually relevant?
'''
- Returns boolean

4️⃣ Conditional Edges / workflows - LangGraph Feature (graph.py)
'''
workflow.add_conditional_edges(...)
'''
- If relevant → go to generate
- If not → go to fallback

5️⃣ Generate Node (generator.py)
- Builds prompt using retrieved context
- Sends to LLM
- Produces grounded answer

6️⃣ Fallback Node
- Returns safe message if retrieval is poor.

## 🛠 How to Extend This Project

This project is intentionally modular and easy to upgrade.

You can extend it by adding:

- Query rewriting node
- Answer verification node
- Self-reflection loop
- Hybrid search (BM25 + vector)
- Streaming responses
- FastAPI deployment
- Docker support
- LangSmith tracing
- Multi-agent orchestration

---

## 🔒 Production Readiness Considerations

For real-world deployment, consider adding:

- Structured logging
- Retry logic
- Observability
- API layer (FastAPI)
- Rate limiting
- Input validation
- Caching
- Monitoring
- Unit tests
- CI/CD pipeline

---

## 🎯 Who This Is For

- Software engineers learning RAG
- AI engineers building production systems
- Developers exploring LangGraph
- Students studying modern AI architectures

---

## 📚 Learning Outcomes

After exploring this repository, you will understand:

- How RAG pipelines work
- Why graph-based workflows are powerful
- How to implement conditional routing in AI systems
- How to structure production-grade AI applications

---

## 📜 License

MIT License

---

## ⭐ If You Found This Useful

Consider starring the repository and sharing it with others exploring AI engineering.

---

**Project Title:**  
Implementing RAG with LangGraph

**Description:**  
Simple yet powerful examples of building Retrieval-Augmented Generation systems using LangGraph, structured in a clean, extensible, production-ready architecture - for educational purposes only.

