from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pathlib import Path


DATA_FOLDER = Path("data/raw_docs")


def load_documents():
    documents = []

    for file_path in DATA_FOLDER.iterdir():

        if file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            documents.extend(docs)

        elif file_path.suffix == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"\nLoaded {len(docs)} documents\n")

    for doc in docs[:3]:
        print(doc.page_content[:300])
        print("---\n")