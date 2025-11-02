from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from sympy.physics.units import temperature

from rag_pipline import build_multi_rag, query_multi_rag
from extractors import load_code, load_html, load_pdfs, load_all, load_db_rows
from config import PG_CONFIG

# Preload data and retrievers
vector_index, bm25, chunks = build_multi_rag()
llm = OpenAI(temperature=0)

# Individual tool functions

def pdf_tool(query: str) -> str:
    pdf_docs = load_pdfs()
    from retriever import build_vector_index, build_bm25_index
    v_index, chunk = build_vector_index(pdf_docs)
    b25 = build_bm25_index(chunk)
    return query_multi_rag(query, v_index, b25, chunk)


def html_tool(query: str) -> str:
    html_docs = load_html()
    from retriever import build_vector_index, build_bm25_index
    v_index, chunk = build_vector_index(html_docs)
    b25 = build_bm25_index(chunk)
    return query_multi_rag(query, v_index, b25, chunk)

def code_tool(query: str) -> str:
    code_docs = load_code()
    from retriever import build_vector_index, build_bm25_index
    v_index, chunk = build_vector_index(code_docs)
    b25 = build_bm25_index(chunk)
    return query_multi_rag(query, v_index, b25, chunk)

def db_tool(query: str) -> str:
    db_docs = load_db_rows(PG_CONFIG)
    from retriever import build_vector_index, build_bm25_index
    v_index, chunk = build_vector_index(db_docs)
    b25 = build_bm25_index(chunk)
    return query_multi_rag(query, v_index, b25, chunk)

def all_sources_tool(query: str) -> str:
    return query_multi_rag(query, vector_index, bm25, chunks)


# Tool definitions

tools = [
    Tool(name="Search PDFs", func=pdf_tool, description="Use when the question is about documentation, manuals or reports."),
    Tool(name="Search HTML Pages", func=html_tool, description="Use when the question relates to website or HTML Content."),
    Tool(name="Search Source Code", func=code_tool, description="Use for code logic or API implementation questions."),
    Tool(name="Search Database Rows", func=db_tool, description="Use for data coming from structured database rows."),
    Tool(name="Search ALL Sources", func=all_sources_tool, description="Default, search all sources when unsure."),
]

# Initialize agent
agent = initialize_agent(tools=tools, llm=llm, agent_type="zero-shot-react-description", verbose=True)

def chat_with_agent(question: str):
    return agent.run(question)

if __name__ == "__main__":
    print(chat_with_agent("Summarize Java microservice code pattern from stored source files."))


"""
API mode

uvicorn server:app --port 8000


Agent mode
python agent.py


| Layer             | Purpose                      | Key file          |
| ----------------- | ---------------------------- | ----------------- |
| Document loaders  | Extract PDFs, HTML, DB, Code | `extractors.py`   |
| Index & retrieval | Pinecone vectors + BM25      | `retriever.py`    |
| Reranking         | Cross-encoder                | `reranker.py`     |
| RAG orchestration | Combine retrievers + LLM     | `rag_pipeline.py` |
| REST API          | Serve via FastAPI            | `server.py`       |
| Agent layer       | Dynamic tool choice          | `agent.py`        |


Next steps

Add authentication and caching (Redis) for the FastAPI layer.

Deploy Pinecone in production tier and tune chunk sizes (use your existing benchmark_chunks.py).

If you prefer a UI, wrap the API with a lightweight Streamlit front end.
"""