# # import os, json, csv
# # from fpdf import FPDF
# #
# # root = "multi-rag-testdata-fake/data"
# # os.makedirs(f"{root}/pdfs", exist_ok=True)
# # os.makedirs(f"{root}/html", exist_ok=True)
# # os.makedirs(f"{root}/code/java", exist_ok=True)
# # os.makedirs(f"{root}/code/python", exist_ok=True)
# # os.makedirs(f"{root}/code/sql", exist_ok=True)
# # os.makedirs(f"{root}/db_rows", exist_ok=True)
# #
# # # --- PDFs ---
# # pdfs = {
# #     "java_fundamentals.pdf": "Java basics, collections, concurrency, streams, JVM tuning.",
# #     "spring_ai_microservices.pdf": "Spring Boot with AI integration, RAG microservices.",
# #     "aws_cloud_architecture.pdf": "AWS Lambda, API Gateway, DynamoDB, S3, CI/CD pipeline.",
# #     "rag_pipeline_design.pdf": "LangChain, Pinecone, chunking, cross-encoder rerankers."
# # }
# # for name, text in pdfs.items():
# #     pdf = FPDF()
# #     pdf.add_page()
# #     pdf.set_font("Arial", size=12)
# #     pdf.multi_cell(0, 10, text)
# #     pdf.output(f"{root}/pdfs/{name}")
# #
# # # --- HTML pages ---
# # html_pages = {
# #     "devops_best_practices.html": "<h1>DevOps Best Practices</h1><p>Use CI/CD, IaC, and observability.</p>",
# #     "websocket_protocols.html": "<h1>WebSocket Protocols</h1><p>STOMP over WebSocket in Java and Python.</p>",
# #     "ml_vs_llm_explained.html": "<h1>ML vs LLM</h1><p>LLMs extend ML with transformer architectures.</p>",
# #     "azure_openai_integration.html": "<h1>Azure OpenAI Integration</h1><p>Deploy GPT models via Azure Cognitive Services.</p>"
# # }
# # for fn, html in html_pages.items():
# #     with open(f"{root}/html/{fn}", "w") as f:
# #         f.write(html)
# #
# # # --- Code samples ---
# # java_code = """public class HashMapExample {
# #     public static void main(String[] args) {
# #         java.util.HashMap<String, Integer> map = new java.util.HashMap<>();
# #         map.put("Java", 11);
# #         map.put("SpringBoot", 3);
# #         System.out.println(map);
# #     }
# # }"""
# # open(f"{root}/code/java/HashMapExample.java", "w").write(java_code)
# #
# # python_code = """from langchain.vectorstores import Pinecone
# # from langchain.embeddings import OpenAIEmbeddings
# #
# # def multi_retriever_query(question):
# #     emb = OpenAIEmbeddings()
# #     store = Pinecone.from_existing_index("tech-index", embedding=emb)
# #     docs = store.similarity_search(question, k=5)
# #     return docs
# # """
# # open(f"{root}/code/python/langchain_multi_retriever.py", "w").write(python_code)
# #
# # sql_schema = """CREATE TABLE incidents(
# #     id SERIAL PRIMARY KEY,
# #     service VARCHAR(100),
# #     summary TEXT,
# #     severity VARCHAR(20),
# #     created_at TIMESTAMP DEFAULT NOW()
# # );"""
# # open(f"{root}/code/sql/postgres_schema.sql", "w").write(sql_schema)
# #
# # # --- DB rows ---
# # incidents = [
# #     {"id": 1, "service": "RAG-Service", "summary": "High latency during model load", "severity": "medium"},
# #     {"id": 2, "service": "ETL", "summary": "Pipeline failed on schema mismatch", "severity": "high"}
# # ]
# # open(f"{root}/db_rows/incidents.json", "w").write(json.dumps(incidents, indent=2))
# #
# # with open(f"{root}/db_rows/embeddings_metadata.csv", "w", newline="") as f:
# #     w = csv.writer(f)
# #     w.writerow(["id", "source", "vector_dim"])
# #     w.writerow([1, "pdf:java_fundamentals", 1536])
# #     w.writerow([2, "html:websocket_protocols", 1536])
#
# # 2 ============================
# # ==================================
#
# #
# # import os, random, json, csv
# # from fpdf import FPDF
# # from faker import Faker
# #
# # fake = Faker()
# # root = "multi-rag-testdata-fake/data"
# #
# # for sub in ["pdfs","html","code/java","code/python","code/sql","db_rows"]:
# #     os.makedirs(f"{root}/{sub}", exist_ok=True)
# #
# # topics = [
# #     "Java Streams", "Spring Boot REST", "LangChain RAG", "Cross-Encoder Rerank",
# #     "AWS Lambda", "Azure OpenAI", "FastAPI", "Redis Caching", "PostgreSQL Tuning",
# #     "MongoDB Indexing", "WebSocket STOMP", "CI/CD Pipelines", "Terraform IaC",
# #     "LLM Fine-tuning", "Prompt Engineering", "DevOps Observability"
# # ]
# #
# # # --- PDFs ---
# # for i, topic in enumerate(topics, 1):
# #     pdf = FPDF()
# #     pdf.add_page()
# #     pdf.set_font("Arial", size=12)
# #     text = f"{topic}\n\n" + "\n".join(fake.paragraphs(nb=5))
# #     pdf.multi_cell(0, 10, text)
# #     pdf.output(f"{root}/pdfs/{topic.replace(' ','_')}.pdf")
# #
# # # --- HTML ---
# # for topic in topics:
# #     html = f"<h1>{topic}</h1>\n<p>{fake.paragraph(nb_sentences=5)}</p>"
# #     with open(f"{root}/html/{topic.replace(' ','_').lower()}.html","w") as f:
# #         f.write(html)
# #
# # # --- Code samples ---
# # for topic in topics:
# #     jfile = f"{root}/code/java/{topic.replace(' ','')}.java"
# #     pfile = f"{root}/code/python/{topic.replace(' ','_').lower()}.py"
# #     sfile = f"{root}/code/sql/{topic.replace(' ','_').lower()}.sql"
# #     open(jfile,"w").write(f"// Example for {topic}\npublic class Example {{ public static void main(String[] a){{ System.out.println(\"{topic}\");}}}}")
# #     open(pfile,"w").write(f"# Example for {topic}\ndef demo():\n    print('{topic}')")
# #     open(sfile,"w").write(f"-- Example query for {topic}\nSELECT * FROM examples WHERE topic='{topic}';")
# #
# # # --- DB rows ---
# # incidents = []
# # for i in range(1,201):
# #     incidents.append({
# #         "id": i,
# #         "service": random.choice(["RAG-Service","ETL","Frontend","ML-Pipeline"]),
# #         "summary": fake.sentence(),
# #         "severity": random.choice(["low","medium","high"]),
# #         "created_at": str(fake.date_time_this_year())
# #     })
# # with open(f"{root}/db_rows/incidents.json","w") as f:
# #     json.dump(incidents,f,indent=2)
# #
# # with open(f"{root}/db_rows/embeddings_metadata.csv","w",newline="") as f:
# #     w = csv.writer(f)
# #     w.writerow(["id","source","vector_dim"])
# #     for i,t in enumerate(topics,1):
# #         w.writerow([i,f"pdf:{t}",1536])
#
#
# # 3============
#
# #!/usr/bin/env python3
# """
# Collect real, license-friendly technical docs for RAG evaluation.
#
# Sources:
# - Python tutorial (PSF License)
# - Spring Boot reference (Apache 2.0)
# - LangChain docs (MIT)
# - AWS Lambda developer guide (CC-BY-SA 4.0)
# - PostgreSQL manual (CC-BY)
# - FastAPI docs (MIT)
#
# Creates folder structure:
# multi-rag-testdata/data/{html,code/java,code/python,db_rows}
# """
# #
# # import os, requests, shutil, subprocess, csv, json
# # from bs4 import BeautifulSoup
# #
# # BASE = "multi-rag-testdata/data"
# # os.makedirs(f"{BASE}/html", exist_ok=True)
# # os.makedirs(f"{BASE}/code/java", exist_ok=True)
# # os.makedirs(f"{BASE}/code/python", exist_ok=True)
# # os.makedirs(f"{BASE}/db_rows", exist_ok=True)
# #
# # # ---------------------------------------------------------------------
# # # 1. Download selected HTML docs
# # # ---------------------------------------------------------------------
# # PAGES = {
# #     "python_tutorial": "https://docs.python.org/3/tutorial/index.html",
# #     "spring_boot_ref": "https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/",
# #     "langchain_intro": "https://python.langchain.com/docs/get_started/introduction",
# #     "aws_lambda": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
# #     "postgresql_manual": "https://www.postgresql.org/docs/current/index.html",
# #     "fastapi": "https://fastapi.tiangolo.com/"
# # }
# #
# # print("Downloading HTML documentation ...")
# # for name, url in PAGES.items():
# #     try:
# #         html = requests.get(url, timeout=40).text
# #         soup = BeautifulSoup(html, "html.parser")
# #         text = soup.get_text(" ", strip=True)
# #         out_file = f"{BASE}/html/{name}.html"
# #         open(out_file, "w", encoding="utf-8").write(text)
# #         print("✔ saved", out_file)
# #     except Exception as e:
# #         print("⚠️  failed", name, e)
# #
# # # ---------------------------------------------------------------------
# # # 2. Clone small open-source repos for code examples
# # # ---------------------------------------------------------------------
# # REPOS = {
# #     "spring-petclinic": "https://github.com/spring-projects/spring-petclinic.git",
# #     "langchain": "https://github.com/langchain-ai/langchain.git",
# #     "fastapi": "https://github.com/tiangolo/fastapi.git",
# # }
# #
# # print("\nCloning open-source repositories (Apache/MIT) ...")
# # for name, repo in REPOS.items():
# #     target = f"tmp_{name}"
# #     if os.path.exists(target):
# #         shutil.rmtree(target)
# #     subprocess.run(["git", "clone", "--depth=1", repo, target], check=False)
# #     if "java" in name:
# #         code_dir = f"{BASE}/code/java"
# #     elif name == "spring-petclinic":
# #         code_dir = f"{BASE}/code/java"
# #     else:
# #         code_dir = f"{BASE}/code/python"
# #     for root, _, files in os.walk(target):
# #         for fn in files:
# #             if fn.endswith((".py", ".java")):
# #                 src = os.path.join(root, fn)
# #                 dst = os.path.join(code_dir, f"{name}_{fn}")
# #                 try:
# #                     shutil.copy(src, dst)
# #                 except Exception:
# #                     pass
# #     shutil.rmtree(target, ignore_errors=True)
# #     print("✔ collected code from", name)
# #
# # # ---------------------------------------------------------------------
# # # 3. Create DB-like JSON/CSV from open data
# # # ---------------------------------------------------------------------
# # print("\nCreating sample DB rows from open Stack Overflow survey snippet ...")
# # sample_rows = [
# #     {"id": 1, "language": "Python", "db": "PostgreSQL", "cloud": "AWS"},
# #     {"id": 2, "language": "Java", "db": "MongoDB", "cloud": "Azure"},
# #     {"id": 3, "language": "Go", "db": "DynamoDB", "cloud": "AWS"},
# # ]
# # with open(f"{BASE}/db_rows/dev_survey.json", "w") as f:
# #     json.dump(sample_rows, f, indent=2)
# #
# # with open(f"{BASE}/db_rows/dev_survey.csv", "w", newline="") as f:
# #     w = csv.DictWriter(f, fieldnames=sample_rows[0].keys())
# #     w.writeheader()
# #     w.writerows(sample_rows)
# #
# # print("\n✅ All data collected under multi-rag-testdata/data/")
# # print("   You can now run your ingestion pipeline on these folders.")
#
# #!/usr/bin/env python3
# """
# Extend real data collector: add Hugging Face model & dataset READMEs
# and AWS Open Data Registry entries.
# """
#
# import os, json, requests
# from bs4 import BeautifulSoup
#
# BASE = "multi-rag-testdata/data"
# os.makedirs(f"{BASE}/ai_hf", exist_ok=True)
# os.makedirs(f"{BASE}/aws_open", exist_ok=True)
#
# # ---------------------------------------------------------------------
# # 1. Hugging Face model cards / dataset READMEs
# # ---------------------------------------------------------------------
# HF_ITEMS = [
#     "bert-base-uncased",
#     "distilbert-base-uncased",
#     "deepset/roberta-base-squad2",
#     "squad",
#     "coqa",
#     "langchain-ai/langchain",
# ]
#
# print("Fetching Hugging Face READMEs...")
# for name in HF_ITEMS:
#     try:
#         url = f"https://huggingface.co/{name}/raw/main/README.md"
#         r = requests.get(url, timeout=30)
#         if r.status_code == 200:
#             out = f"{BASE}/ai_hf/{name.replace('/', '_')}.md"
#             open(out, "w", encoding="utf-8").write(r.text)
#             print("✔", name)
#         else:
#             # try dataset info API as fallback
#             info = requests.get(f"https://huggingface.co/api/models/{name}", timeout=20).json()
#             out = f"{BASE}/ai_hf/{name.replace('/', '_')}.json"
#             json.dump(info, open(out, "w"), indent=2)
#             print("✔ API metadata", name)
#     except Exception as e:
#         print("⚠️", name, e)
#
# # ---------------------------------------------------------------------
# # 2. AWS Open Data Registry entries
# # ---------------------------------------------------------------------
# AWS_DATASETS = [
#     "amazon-reviews-pds",
#     "commoncrawl",
#     "open-images-dataset",
# ]
#
# print("\nFetching AWS Open Data Registry metadata...")
# for ds in AWS_DATASETS:
#     try:
#         url = f"https://registry.opendata.aws/{ds}/"
#         html = requests.get(url, timeout=30).text
#         soup = BeautifulSoup(html, "html.parser")
#         text = soup.get_text(" ", strip=True)
#         out = f"{BASE}/aws_open/{ds}.txt"
#         open(out, "w", encoding="utf-8").write(text)
#         print("✔", ds)
#     except Exception as e:
#         print("⚠️", ds, e)
#
# print("\n✅ Hugging Face and AWS Open Data samples saved under:")
# print("   multi-rag-testdata/data/ai_hf/")
# print("   multi-rag-testdata/data/aws_open/")
#


#!/usr/bin/env python3
"""
Unified real-data collector for multi-RAG pipelines.
Creates: multi-rag-testdata/data/{html,code/java,code/python,db_rows,ai_hf,aws_open}
Sources:
- Python, Spring Boot, LangChain, FastAPI, AWS Lambda, PostgreSQL docs
- Spring PetClinic, LangChain, FastAPI repos
- Example DB rows
- Hugging Face model & dataset READMEs
- AWS Open Data Registry metadata
"""

import os, requests, shutil, subprocess, json, csv
from bs4 import BeautifulSoup

BASE = "multi-rag-testdata/data"
for sub in ["html", "code/java", "code/python", "db_rows", "ai_hf", "aws_open"]:
    os.makedirs(f"{BASE}/{sub}", exist_ok=True)

# ---------------------------------------------------------------------
# 1. Download documentation HTML
# ---------------------------------------------------------------------
DOCS = {
    "python_tutorial": "https://docs.python.org/3/tutorial/index.html",
    "spring_boot_ref": "https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/",
    "langchain_intro": "https://python.langchain.com/docs/get_started/introduction",
    "aws_lambda": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    "postgresql_manual": "https://www.postgresql.org/docs/current/index.html",
    "fastapi": "https://fastapi.tiangolo.com/",
}

print("🔹 Downloading documentation HTML ...")
for name, url in DOCS.items():
    try:
        html = requests.get(url, timeout=40).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        out = f"{BASE}/html/{name}.html"
        open(out, "w", encoding="utf-8").write(text)
        print("✔", name)
    except Exception as e:
        print("⚠️", name, e)

# ---------------------------------------------------------------------
# 2. Clone open-source repos for code examples
# ---------------------------------------------------------------------
REPOS = {
    "spring-petclinic": "https://github.com/spring-projects/spring-petclinic.git",
    "langchain": "https://github.com/langchain-ai/langchain.git",
    "fastapi": "https://github.com/tiangolo/fastapi.git",
}

print("\n🔹 Cloning open-source repositories ...")
for name, repo in REPOS.items():
    tmp = f"tmp_{name}"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    subprocess.run(["git", "clone", "--depth=1", repo, tmp], check=False)
    code_dir = f"{BASE}/code/java" if name == "spring-petclinic" else f"{BASE}/code/python"
    for root, _, files in os.walk(tmp):
        for fn in files:
            if fn.endswith((".java", ".py")):
                src = os.path.join(root, fn)
                dst = os.path.join(code_dir, f"{name}_{fn}")
                try:
                    shutil.copy(src, dst)
                except Exception:
                    pass
    shutil.rmtree(tmp, ignore_errors=True)
    print("✔", name)

# ---------------------------------------------------------------------
# 3. Sample DB-like JSON/CSV
# ---------------------------------------------------------------------
rows = [
    {"id": 1, "language": "Python", "db": "PostgreSQL", "cloud": "AWS"},
    {"id": 2, "language": "Java", "db": "MongoDB", "cloud": "Azure"},
    {"id": 3, "language": "Go", "db": "DynamoDB", "cloud": "AWS"},
]
with open(f"{BASE}/db_rows/dev_survey.json", "w") as f:
    json.dump(rows, f, indent=2)
with open(f"{BASE}/db_rows/dev_survey.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("\n✔ Sample DB rows created.")

# ---------------------------------------------------------------------
# 4. Hugging Face model cards / dataset READMEs
# ---------------------------------------------------------------------
HF_ITEMS = [
    "bert-base-uncased",
    "distilbert-base-uncased",
    "deepset/roberta-base-squad2",
    "squad",
    "coqa",
    "langchain-ai/langchain",
]

print("\n🔹 Fetching Hugging Face READMEs ...")
for name in HF_ITEMS:
    try:
        url = f"https://huggingface.co/{name}/raw/main/README.md"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            out = f"{BASE}/ai_hf/{name.replace('/', '_')}.md"
            open(out, "w", encoding="utf-8").write(r.text)
            print("✔", name)
        else:
            info = requests.get(f"https://huggingface.co/api/models/{name}", timeout=20).json()
            out = f"{BASE}/ai_hf/{name.replace('/', '_')}.json"
            json.dump(info, open(out, "w"), indent=2)
            print("✔ API info", name)
    except Exception as e:
        print("⚠️", name, e)

# ---------------------------------------------------------------------
# 5. AWS Open Data Registry entries
# ---------------------------------------------------------------------
AWS_DATASETS = [
    "amazon-reviews-pds",
    "commoncrawl",
    "open-images-dataset",
]

print("\n🔹 Fetching AWS Open Data Registry metadata ...")
for ds in AWS_DATASETS:
    try:
        url = f"https://registry.opendata.aws/{ds}/"
        html = requests.get(url, timeout=30).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        out = f"{BASE}/aws_open/{ds}.txt"
        open(out, "w", encoding="utf-8").write(text)
        print("✔", ds)
    except Exception as e:
        print("⚠️", ds, e)

print("\n✅ All data collected under multi-rag-testdata/data/")
