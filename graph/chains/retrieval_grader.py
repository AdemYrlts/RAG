from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from ingestion import retriever


class GradeDocuments(BaseModel):
    """
    Binary score for relevance check on retrieved documents.
    """
    binary_score: str = Field(
        ...,
        description="Documents are relevant to the question, 'yes' or 'no'",
    )


llm = OllamaLLM(model="cogito:8b", temperature=0)

system_prompt = """
You are grader assessing whether an LLM generation is grounded / supported by a set of retrieved facts.
If the document contains keyword or semantic meaning related to the question, grade it as relevant.
Give a binary score 'yes' or 'no'. 
'yes' means that the answer is grounded in / supported by the set of facts. 

Return ONLY valid JSON like this:
{{"binary_score": "yes"}}
or
{{"binary_score": "no"}}
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Retrieved document: {document}\nUser question: {question}")
    ]
)

parser = JsonOutputParser(pydantic_object=GradeDocuments)
retrieval_grader = grade_prompt | llm | parser





