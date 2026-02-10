from typing import List, TypedDict, Optional
class GraphState(TypedDict,total=False):
    """
    Represents state of graph
    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search or not
        documents: list of documents
    """
    question: str
    generation: Optional[str]
    web_search: Optional[bool]
    documents: List[str]