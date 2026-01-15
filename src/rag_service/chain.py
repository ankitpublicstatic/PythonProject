import asyncio
from retrievers import multi_retrieve
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

async def get_answer(query: str):
    docs = await multi_retrieve(query, top_k=50, top_n = 5)
    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"You are a precise assistant. Use only the context to answer.\n\nContext:\n{context}\n\nQuestion:{query}"
    return llm(prompt)
