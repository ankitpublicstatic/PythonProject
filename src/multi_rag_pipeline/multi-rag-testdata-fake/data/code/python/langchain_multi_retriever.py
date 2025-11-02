from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

def multi_retriever_query(question):
    emb = OpenAIEmbeddings()
    store = Pinecone.from_existing_index("tech-index", embedding=emb)
    docs = store.similarity_search(question, k=5)
    return docs
