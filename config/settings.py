import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    #API Key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment variables")

    #Models
    LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
    EMBEDDING_MODEL = "Alibaba-NLP/gte-multilingual-base"

    #Vector DB
    CHROMA_PERSIST_DIR = "chroma_db"
    COLLECTION_NAME = "policy_docs"
    DATA_DIR = "data"

settings = Settings()