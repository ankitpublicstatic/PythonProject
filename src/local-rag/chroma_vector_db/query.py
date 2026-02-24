import torch
from langchain_community.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Use Apple Metal if available
device = "mps" if torch.backends.mps.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device},
)

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model,
)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})

llm = ChatOllama(
    model="llama3:8b",
    temperature=0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
)

while True:
    query = input("Ask: ")
    result = qa.ask(query)
    print("\nAnswer: ", result)
