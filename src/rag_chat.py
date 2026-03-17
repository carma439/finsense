from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from langchain_groq import ChatGroq
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough

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
        search_kwargs={"k": 3}
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_template("""
            You are a financial assistant.

            Use the context below to answer the user's question. Do not provide Document Id in the answer and start answer directly without explicitly mentioning context.

            Context:
            {context}

            Question:
            {question}
            
            If you cannot find relevant information in context, say you do not know. Never guess and go beyond the context.
            """)

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


if __name__ == "__main__":

    rag = build_rag()

    while True:

        query = input("\nAsk a question (or 'exit'): ")

        if query == "exit":
            break

        answer = rag.invoke(query)

        print("\nAnswer:\n")
        print(answer)
        
        
        