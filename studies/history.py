from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = OllamaLLM(model="cogito:8b", temperature=0.1)

store = {}

def get_session_history(session_id : str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="messages")
    ]
)
chain = prompt | llm
config = {"configurable" : {"session_id" : "1"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)
if __name__ == "__main__":
    while True:
        user_input = input("-> ")
        response = with_message_history.invoke(
            [
                HumanMessage(content = user_input)
            ],
            config = config,
        )
        print(response)