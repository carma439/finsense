from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

from ingest import load_documents
from text_cleaner import clean_text

load_dotenv()

def build_vector_db():

    print("Loading documents...")
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")
    
    print("Cleaning documents...")
    
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    print("Cleaned documents")
    
    print("Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Building vector database...")

    vectorstore = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    print("Vector database created!")

    return vectorstore


if __name__ == "__main__":
    build_vector_db()