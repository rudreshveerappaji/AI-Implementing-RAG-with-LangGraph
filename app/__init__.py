"""
Implementing RAG with LangGraph

This package contains all core application modules required to run the
graph-based Retrieval-Augmented Generation (RAG) system.

Modules exposed here allow clean imports when using:
    python -m app.main

Keeping this file minimal avoids side effects during import.
"""

__version__ = "1.0.0"

# Optional: expose commonly used components for cleaner imports
# from .graph import build_graph
# from .retriever import build_vector_store, load_vector_store

"""
__init__.py is a special Python file that:

1. Marks a directory as a Python package
2. Controls what gets exposed when importing the package
3. Can run initialization logic (if needed)
4. Defines package-level variables (like version)

__init__.py runs automatically when you import the package.

Without init py, you will need to do this in a src file:

from .graph import build_graph
__all__ = ["build_graph"]

But if you create init py file, you can do this:

from app import build_graph

So in summary, if you have a folder like this:

app/

Without __init__.py → app/ is just a folder
With __init__.py → app/ becomes a Python module

"""
