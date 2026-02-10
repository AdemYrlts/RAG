from graph.nodes.generate import generate_func
from graph.nodes.grader_documents import grade_documents
from graph.nodes.web_search import web_search
from graph.nodes.retrieve import retrieve
from graph.chains.router import question_router, RouteQuery
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

def test_documents_relevant(state:GraphState):
    print("---ASSESS GRADED DOCUMENTS---")
    if state["web_search"]:
        print("websearch")
        return "websearch"
    else:
        return "generate"

def test_hallucinations_and_answer(state:GraphState):
    question = state["question"]
    generation = state["generation"]
    documents = state["documents"]
    score_hall = hallucination_grader.invoke({"documents":documents, "generation":generation})
    if score_hall["binary_score"].lower() == "yes":
        print("GENERATION IS GROUNDED IN DOCUMENTS")
        score_ans = answer_grader.invoke({"question":question,"generation":generation})
        if score_ans["binary_score"].lower() == "yes":
            print("GENERATION ADDRESSES QUESTION")
            return "useful"
        else:
            print("GENERATION DOES NOT ADDRESSES QUESTION")
            return "not useful"
    else:
        print("GENERATION IS NOT GROUNDED IN DOCUMENTS")
        return "not supported"

def test_router(state: GraphState):
    question = state["question"]
    source = question_router.invoke({"question": question})
    if isinstance(source, dict):  # JSON parse edilemedi
        source = RouteQuery(**source)  # dict → model
    if source.datasource == "vectorstore":
        print("vectorstore")
        return "retrieve"
    else:
        print("websearch")
        return "websearch"




workflow = StateGraph(GraphState)
workflow.add_node("generate", generate_func)
workflow.add_node("retrieve", retrieve)
workflow.add_node("websearch", web_search)
workflow.add_node("grader_documents", grade_documents)

workflow.add_conditional_edges(
    "grader_documents",
    test_documents_relevant,
    {"websearch":"websearch","generate":"generate"}
)
workflow.add_conditional_edges(
    "generate",
    test_hallucinations_and_answer,
    {"not supported": "generate","useful": END,"not useful": "websearch"}
)
workflow.set_conditional_entry_point(
    test_router,
    {"retrieve": "retrieve","websearch":"websearch"}
)
workflow.add_edge("retrieve","grader_documents")
workflow.add_edge("websearch","generate")
workflow.add_edge("generate",END)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")