import os
from dotenv import load_dotenv
import pinecone

load_dotenv()

# Environment

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment = os.getenv("PINECONE_ENV"))
INDEX_NAME = "multi-rag-index"

# PostgreSQL
PG_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASS"),
    "database": os.getenv("PG_DB")
}