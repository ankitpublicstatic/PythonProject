import os
import torch
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredFileLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# ===============================
# 1️⃣ Apple Metal Optimization
# ===============================

device = "mps" if torch.backends.mps.is_available() else "cpu"

# ===============================
# 2️⃣ Embedding Model
# ===============================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

# ===============================
# 3️⃣ Load Documents
# ===============================

def load_documents(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())

        elif file.endswith(".txt") or file.endswith(".sql"):
            docs.extend(TextLoader(path).load())

        elif file.endswith(".html"):
            docs.extend(UnstructuredHTMLLoader(path).load())

        elif file.endswith(".docx"):
            docs.extend(UnstructuredFileLoader(path).load())

        # For audio/video -> transcription required
        elif file.endswith((".mp3", ".wav", ".mp4", ".mkv")):
            from whisper import load_model
            whisper_model = load_model("base")
            result = whisper_model.transcribe(path)
            docs.append({"page_content": result["text"], "metadata": {"source": file}})

    return docs

# ===============================
# 4️⃣ Text Splitting
# ===============================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# ===============================
# 5️⃣ Build / Load Chroma
# ===============================

PERSIST_DIR = "chroma_db"

def build_vectorstore(docs):
    chunks = text_splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )
    vectordb.persist()
    return vectordb

# ===============================
# 6️⃣ Load LLM (Llama3:8B)
# ===============================

llm = Ollama(
    model="llama3:8b",
    temperature=0,
)

# ===============================
# 7️⃣ RAG Chain
# ===============================

def create_rag_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

# ===============================
# 8️⃣ Run
# ===============================

if __name__ == "__main__":
    folder = "./documents"

    if not os.path.exists(PERSIST_DIR):
        documents = load_documents(folder)
        vectordb = build_vectorstore(documents)
    else:
        vectordb = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding_model
        )

    qa = create_rag_chain(vectordb)

    while True:
        query = input("\nAsk: ")
        result = qa({"query": query})
        print("\nAnswer:\n", result["result"])