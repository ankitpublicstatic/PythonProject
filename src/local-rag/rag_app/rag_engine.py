
import torch
import time
from tracing import tracer
import matplotlib.pyplot as plt
from rank_bm25 import BM25Okapi
from utils.token_usage import calculate_usage
from sentence_transformers import CrossEncoder
from redis_cache import get_cache, set_cache
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "chroma_db"

device = "mps" if torch.backends.mps.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)
# model_name="sentence-transformers/all-MiniLM-L6-v2")

vectordb = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embedding_model
)

# Now you can re-ingest documents with new version without deleting old ones.
# Metadata Filtering
# You can filter by: filename tags document type

# retriever = vectordb.as_retriever(
#     search_kwargs={
#         "k": 5,
#         "filter": {"source": "data/dsa.pdf", "version": "v2"},
#     }
# )

retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# Reranker model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Chat LLM
llm = ChatOllama(
    model="llama3:8b",
    temperature=0,
    streaming=True
)

chat_history = []

def hybrid_search(query):
    # Retrieve top 8 related query documents from vector store(Chroma DB)
    vector_docs = retriever.invoke(query)

    corpus = [doc.page_content for doc in vector_docs]
    bm25 = BM25Okapi([doc.split() for doc in corpus])
    scores = bm25.get_scores(query.split())

    # Combine vector + bm25
    ranked = sorted(zip(vector_docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:5]]

def rerank(query, docs):
    pairs = [[query, d.page_content] for d in docs]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    # visualize_scores(docs, scores)

    return [doc for doc, _ in ranked[:3]]

def visualize_scores(docs, scores):
    labels = [f"Chunk {i}" for i in range(len(scores))]
    plt.bar(labels, scores)
    plt.title("Chunk Relevance Scores")
    plt.xticks(rotation=45)
    plt.show()

async def stream_answer(query):
    cached = get_cache(query)
    if cached:
        print("⚡ From Cache\n")
        print(cached)
        yield cached
        return
    # normal RAG flow ...
    docs = hybrid_search(query)
    docs = rerank(query, docs)

    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"""
                    You are a precise assistant.
                    Use only the context below.

                    Context:
                    {context}

                    Chat History:
                    {chat_history}

                    Question:
                    {query}
                    """
    response = llm.stream(prompt)
    for chunk in response:
        yield chunk.content

    # full_response = ""
    # for chunk in response:
    #     print(chunk.content, end="", flush=True)
    #     full_response += chunk.content
    #
    # chat_history.append({"question": query, "answer": full_response})
    #
    # set_cache(query, full_response)
    # print("\n")



def stream_answer_on_console(query: str):
    start_time = time.time()
    cached = get_cache(query)
    if cached:
        print("⚡ From Cache\n")
        print(cached)
        return

    # normal RAG flow ...
    global chat_history
    with tracer.start_as_current_span("retrieval"):
        docs = hybrid_search(query)

    with tracer.start_as_current_span("reranking"):
        docs = rerank(query, docs)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
                You are a precise assistant.
                Use only the context below.
                
                Context:
                {context}
                
                Chat History:
                {chat_history}
                
                Question:
                {query}
                """
    with tracer.start_as_current_span("llm_generation"):
        response = llm.stream(prompt)

    full_response = ""
    for chunk in response:
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    chat_history.append({"question": query, "answer": full_response})

    set_cache(query, full_response)
    print("\n")

    end_time = time.time()

    # Token usage calculation
    # usage = calculate_usage(prompt, full_response)
    # usage = {
    #     "prompt_tokens": response.response_metadata["prompt_eval_count"],
    #     "completion_tokens": response.response_metadata["eval_count"],
    #     "total_tokens": (
    #             response.response_metadata["prompt_eval_count"]
    #             + response.response_metadata["eval_count"]
    #     )
    # }
    # print("========TOKEN USAGE 1========")
    # print(usage)
    # usage = {
    #     "prompt_tokens": meta.get("prompt_eval_count", 0),
    #     "completion_tokens": meta.get("eval_count", 0),
    # }
    #
    # usage["total_tokens"] = (
    #         usage["prompt_tokens"] + usage["completion_tokens"]
    # )
    # print("========TOKEN USAGE 2========")
    # print(usage)
    # print("Latency:", round(end_time - start_time, 2), "seconds")
    # print("===================")
    #
    # print("\n")


def generate_answer(query: str):
    start_time = time.time()
    cached = get_cache(query)
    if cached:
        print("⚡ From Cache\n")
        print(cached)
        return

    # normal RAG flow ...
    global chat_history
    with tracer.start_as_current_span("retrieval"):
        docs = hybrid_search(query)

    with tracer.start_as_current_span("reranking"):
        docs = rerank(query, docs)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
                You are a precise assistant.
                Use only the context below.

                Context:
                {context}

                Chat History:
                {chat_history}

                Question:
                {query}
                """
    with tracer.start_as_current_span("llm_generation"):
        response = llm.invoke(prompt)

    meta = response.response_metadata
    response_dict = {
        "content": response.content,
        "additional_kwargs": response.additional_kwargs,
        "response_metadata": response.response_metadata,
        "type": response.type,
    }
    chat_history.append({"question": query, "answer": response.content})

    set_cache(query, response_dict)
    print("\n")

    end_time = time.time()

    # Token usage calculation
    # usage = calculate_usage(prompt, full_response)
    usage = {
        "prompt_tokens": response.response_metadata["prompt_eval_count"],
        "completion_tokens": response.response_metadata["eval_count"],
        "total_tokens": (
                response.response_metadata["prompt_eval_count"]
                + response.response_metadata["eval_count"]
        )
    }
    print("========TOKEN USAGE 1========")
    print(usage)
    usage = {
        "prompt_tokens": meta.get("prompt_eval_count", 0),
        "completion_tokens": meta.get("eval_count", 0),
    }

    usage["total_tokens"] = (
            usage["prompt_tokens"] + usage["completion_tokens"]
    )
    print("========TOKEN USAGE 2========")
    print(usage)
    print("Latency:", round(end_time - start_time, 2), "seconds")
    print("===================")

    print("\n")
    return {
        "answer": response,
        "usage": usage,
        "latency_in_seconds": round(end_time - start_time, 2)
    }


prompt = ChatPromptTemplate.from_template("""
            You are a helpful assistant.

            Chat History:
            {history}

            Context:
            {context}

            Question:
            {input}
            """)


def format_history(messages):
    history_text = ""
    for m in reversed(messages):
        history_text += f"{m.role}: {m.content}\n"
    return history_text


def generate_answer_quick(query: str, history_messages):
    history_text = format_history(history_messages)

    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])

    final_prompt = prompt.invoke({
        "history": history_text,
        "context": context,
        "input": query
    })

    response = llm.invoke(final_prompt)

    return response.content
#
# while True:
#     query = input("Ask: ")
#     with tracer.start_as_current_span("stream_answer"):
#         generate_answer(query)
#     # chat_history.append({"question": query, "answer": ""})
#     print("\n")

