from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
import json
from langchain_core.output_parsers import JsonOutputParser

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant datasource.
    """
    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore",
    )


llm = OllamaLLM(model="cogito:8b", temperature=0)

system_prompt = """
You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search.
Return ONLY valid JSON like this:
{{"datasource": "vectorstore"}}
or
{{"datasource": "websearch"}}
"""



route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}")
    ]
)


raw_chain = route_prompt | llm

parser = JsonOutputParser(pydantic_object=RouteQuery)
question_router = route_prompt | llm | parser


