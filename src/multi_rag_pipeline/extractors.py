import os
import psycopg2
import pdfplumber
from bs4 import BeautifulSoup
from langchain.schema import Document
from sqlalchemy.testing.suite.test_reflection import metadata


def load_pdfs(folder="data/pdfs"):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            with pdfplumber.open(os.path.join(folder, file)) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                docs.append(Document(page_content=text, metadata={"source":file, "type":"pdf"}))
    return docs

def load_html(folder="data/html"):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".html"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                text = soup.get_text(separator= " ")
                docs.append(Document(page_content=text, metadata={"source":file,"type": "html"}))
    return docs

def load_code(folder="data/code"):
    docs = []
    for file in os.listdir(folder):
        if file.endswith((".py", ".java", ".js")):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                docs.append(Document(page_content=f.read(), metadata={"source":file, "type": "code"}))
    return docs

def load_db_rows(config):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content from documents;")
    rows = cursor.fetchall()
    conn.close()
    return [Document(page_content=row[1], metadata={"source": f"db_row_{row[0]}", "type": "db"}) for row in rows]

def load_all(config):
    return load_pdfs() + load_html() + load_code() + load_db_rows(config)