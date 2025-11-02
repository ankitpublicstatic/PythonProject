from http.client import responses

import streamlit as st
import requests
from faiss.contrib.datasets import username

API_BASE_URL = os.environ.get("API_BASE_URL")

st.set_page_config(page_title="Multi Source RAG Demo", layout="wide")
st.title("Multi Source RAG Assistant")

# Authentication
st.sidebar.header("Login")
if "token" not in st.session_state:
    username = st.sidebar.text_input("Username", value="admin")
    password = st.sidebar.text_input("Password", type="password", value="User@123")

    if st.sidebar.button("Login"):
        responses = requests.post(f"{API_BASE_URL}/token", data={"username": username, "password": password})
        if responses.status_code == 200:
            st.session_state["token"] = responses.json()["access_token"]
            st.sidebar.success("Logged in as {}".format(username))
        else:
            st.sidebar.error("Login failed")


# Main Query
if "token" in st.session_state:
    query = st.text_area("Enter your Question:", height=120)
    if st.button("Ask"):
        if query.strip():
            with st.spinner("Retrieving and generating answers..."):
                #headers = {"Authorization": "Bearer {}".format(st.session_state["token"])}
                headers = {"Authorization": f"Bearer {(st.session_state['token'])}"}
                response = requests.post(f"{API_BASE_URL}/rag/query", headers=headers,json={"query": query})
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(f"### ✅ Answer:")
                    st.write(data["answer"])
                    if data.get("cached"):
                        st.info("Response served from Redis cache")
                else:
                    st.error(f"Error: {response.text}")

else:
    st.warning("Please Login first")

"""
Run
streamlit run ui_app.py


"""