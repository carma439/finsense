from langchain.tools import tool

from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
from src.logger import get_logger

logger = get_logger("rag_tool")

load_dotenv()

def build_rag():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 2}
    )


    return retriever


retriever = None

# LAZY LOADER FUNCTION
def get_retriever():
    global retriever

    if retriever is None:
        logger.info("Loading RAG system...")
        retriever = build_rag()
        logger.info("RAG system loaded")

    return retriever

@tool
def rag_search(query: str) -> str:
    """
    Search the financial policy knowledge base.

    Use this tool to answer questions about:
    - savings schemes
    - government financial policies
    - tax rules
    - budget changes 

    Input should be the user's question as a string.
    """
    
    logger.info(f"RAG search query: {query}")
    
    retriever = get_retriever()
    
    docs = retriever.invoke(query)

    logger.info(f"Documents retrieved: {len(docs)}")

    if not docs:
        return "No relevant information found in the knowledge base."

    context = "\n\n".join(
        f"Document {i+1}:\n{doc.page_content[:500]}"
        for i, doc in enumerate(docs)
    )
    
    return context