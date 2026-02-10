from langchain import hub
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="cogito:8b", temperature=0)
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()