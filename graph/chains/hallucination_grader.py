from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser



class GradeHallucinations(BaseModel):
    """
    Binary score for hallucination present in generated answers.
    """
    binary_score: str = Field(
        ...,
        description="Answer is grounded in the facts, 'yes' or 'no'",
    )


llm = OllamaLLM(model="cogito:8b", temperature=0)

system_prompt = """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'yes' means that the answer is grounded in / supported by a set of retrieved facts.
Return ONLY valid JSON like this:
{{"binary_score": "yes"}}
or
{{"binary_score": "no"}}
"""



hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation : {generation}")
    ]
)

parser = JsonOutputParser(pydantic_object=GradeHallucinations)
hallucination_grader = hallucination_prompt | llm | parser


