import os
import torch
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    Docx2txtLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Use Apple Metal if available
device = "mps" if torch.backends.mps.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

def load_documents(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif file.endswith(".txt") or file.endswith(".sql"):
            loader = TextLoader(path)
        elif file.endswith(".docx"):
            loader = Docx2txtLoader(path)
        elif file.endswith(".html"):
            loader = UnstructuredHTMLLoader(path)
        else:
            continue

        documents.extend(loader.load())

    return documents


def create_vector_store():
    docs = load_documents("data")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory="chroma_db"
    )

    vectordb.persist()
    print("✅ Vector store created successfully.")


if __name__ == "__main__":
    create_vector_store()