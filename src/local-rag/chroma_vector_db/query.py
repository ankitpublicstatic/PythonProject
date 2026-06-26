import torch
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# ----------------------------
# 1️⃣ Device (Apple Metal)
# ----------------------------
device = "mps" if torch.backends.mps.is_available() else "cpu"

# ----------------------------
# 2️⃣ Embedding Model
# ----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

# ----------------------------
# 3️⃣ Load Persistent Chroma DB
# ----------------------------
vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# ✅ CREATE RETRIEVER (THIS WAS MISSING)
retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# ----------------------------
# 4️⃣ LLM (Ollama Llama3 8B)
# ----------------------------
llm = ChatOllama(
    model="llama3:8b",
    temperature=0
)

# ----------------------------
# 5️⃣ Prompt Template
# ----------------------------
prompt = ChatPromptTemplate.from_template("""
You are a precise assistant.
Answer ONLY from the provided context.
If the answer is not in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{input}
""")

# ----------------------------
# 6️⃣ Create Chains
# ----------------------------
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# ----------------------------
# 7️⃣ Interactive Loop
# ----------------------------
print("🔎 Local RAG Ready. Type 'exit' to quit.\n")

while True:
    query = input("Ask: ")

    if query.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    response = retrieval_chain.invoke({"input": query})

    print("\nAnswer:\n", response["answer"])
    print("\n" + "-" * 50 + "\n")