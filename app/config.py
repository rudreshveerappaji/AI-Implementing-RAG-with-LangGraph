"""
Configuration module.

Loads environment variables and centralizes configuration
to avoid hardcoding secrets or parameters.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please configure it in .env")

# Model configuration
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.0

# Vector DB settings
CHROMA_COLLECTION_NAME = "rag_collection"
PERSIST_DIRECTORY = "./chroma_db"
