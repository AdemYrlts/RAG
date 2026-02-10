from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = OllamaLLM(model="cogito:8b", temperature=0.1)
search = TavilySearchResults(max_results=2)
prompt = hub.pull("hwchase17/react")
tools = [search]

agent = create_react_agent(llm, tools, prompt=prompt)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

if __name__ == "__main__":
    while True:
        user_input = input("> ")
        result = agent_executor.invoke({"input": user_input})
        print(result["output"])

