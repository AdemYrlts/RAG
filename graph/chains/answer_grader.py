from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser



class GradeAnswer(BaseModel):
    binary_score: str = Field(
        ...,
        description="Answer addresses the question, 'yes' or 'no'",
    )


llm = OllamaLLM(model="cogito:8b", temperature=0)

system_prompt = """
You are a grader assessing whether an answer addresses / resolves a question.
Give a binary score 'yes' or 'no'. 'yes' means means that the answer resolves the question.
Return ONLY valid JSON like this:
{{"binary_score": "yes"}}
or
{{"binary_score": "no"}}
"""



answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "User question: \n\n {question} \n\n LLM generation : {generation}")
    ]
)

parser = JsonOutputParser(pydantic_object=GradeAnswer)
answer_grader = answer_prompt | llm | parser


