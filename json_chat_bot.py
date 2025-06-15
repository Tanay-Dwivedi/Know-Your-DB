# json_chat_bot.py

import streamlit as st
import json
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_together import Together
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def handle_json_chat(uploaded_file, api_key):
    # Session state
    if "history" not in st.session_state:
        st.session_state.history = []

    # Load JSON
    try:
        json_data = json.load(uploaded_file)
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON file.")
        return

    # Convert JSON to LangChain Documents
    def json_to_docs(data):
        docs = []
        if isinstance(data, list):
            for item in data:
                content = "\n".join([f"{k}: {v}" for k, v in item.items()])
                docs.append(Document(page_content=content))
        elif isinstance(data, dict):
            content = "\n".join([f"{k}: {v}" for k, v in data.items()])
            docs.append(Document(page_content=content))
        return docs

    documents = json_to_docs(json_data)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Custom prompt to reduce irrelevant info
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Use the context to answer the question as clearly and concisely as possible.
Only answer based on the provided context. Avoid unrelated information.

Context:
{context}

Question: {question}
Answer:
"""
    )

    # LLM setup
    llm = Together(
        together_api_key=api_key,
        model="mistralai/Mistral-7B-Instruct-v0.2",
        temperature=0.7
    )

    # QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    # Chat input
    query = st.text_input("💬 Ask a question about the uploaded JSON:")

    if query:
        try:
            result = qa_chain.invoke(query)
            st.session_state.history.append((query, result["result"]))
        except Exception as e:
            st.error(f"❌ Error generating answer: {str(e)}")

    # Display chat history
    for q, a in st.session_state.history:
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 Bot:** {a}")
