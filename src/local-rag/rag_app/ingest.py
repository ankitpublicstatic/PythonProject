import datetime
import torch
import asyncio
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_DIR = "data"
DB_DIR = "chroma_db"

device = "mps" if torch.backends.mps.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

def load_file(path):
    if path.suffix == ".pdf":
        return PyPDFLoader(str(path)).load()
    elif path.suffix in [".txt", ".sql"]:
        return TextLoader(str(path)).load()
    elif path.suffix == ".docx":
        return Docx2txtLoader(str(path)).load()
    elif path.suffix == ".html":
        return UnstructuredHTMLLoader(str(path)).load()
    else:
        return []


def ingest():
    documents = []

    for file in Path(DATA_DIR).glob("**/*"):
        if file.is_file():
            docs = load_file(file)
            for d in docs:
                d.metadata["source"] = str(file)
                d.metadata["version"] = "v2"
                d.metadata["timestamp"] = datetime.utcnow().isoformat()
            documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)


    vectordb = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=DB_DIR
    )

    # vectordb.persist()
    print("✅ Ingestion complete")


async def ingest_async():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, ingest)


if __name__ == "__main__":
    ingest_async()