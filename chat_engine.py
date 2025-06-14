from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_ollama import OllamaLLM  # ✅ Updated import
import json

def load_json_context_from_file(uploaded_file) -> str:
    data = json.load(uploaded_file)
    return json.dumps(data, indent=2)

def get_chat_chain(json_context: str) -> Runnable:
    template = """
You are a helpful assistant for a classroom database stored in JSON format.

JSON data:
{json_context}

Answer the following question based on the above data.
Question: {question}
Answer:
"""
    prompt = PromptTemplate.from_template(template)
    llm = OllamaLLM(model="openchat")  # ✅ Updated usage
    return prompt | llm
