import uvicorn
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes

llm = OllamaLLM(model="cogito:8b", temperature=0.1)
system_prompt = " Only Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{text}")
    ]
)
parser = StrOutputParser()
chain = prompt_template | llm | parser

app = FastAPI(
    title= "Translation Chat bot"

)
add_routes(app, chain,
           path="/chain")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
