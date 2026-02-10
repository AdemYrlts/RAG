from langchain_ollama import OllamaLLM, OllamaEmbeddings
import bs4
from langchain import hub
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="cogito:8b", temperature=0.1)

loader = WebBaseLoader(
    web_path= ["https://lilianweng.github.io/posts/2023-06-23-agent/"],
    bs_kwargs=dict(
        parse_only = bs4.SoupStrainer(
            class_= ("post-content","post-title","post-header")
        )
    )
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits,embedding=OllamaEmbeddings(model="cogito:8b"))
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context" : retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    for chunk in rag_chain.stream("what is task decomposition"):
        print(chunk)
