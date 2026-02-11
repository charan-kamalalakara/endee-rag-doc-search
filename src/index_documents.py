# src/index_documents.py

from ingest import load_documents
from embedder import Embedder
from vector_store import create_index, store_vectors
from config import INDEX_NAME

DATA_FOLDER = "data/documents"


def main():
    print("Starting document indexing process...")

    # 1. Load documents
    documents = load_documents(DATA_FOLDER)
    print(f"Loaded {len(documents)} documents")

    if not documents:
        print("No documents found. Exiting.")
        return

    # 2. Extract text content
    texts = [doc["content"] for doc in documents]

    # 3. Generate embeddings
    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)
    print("Embeddings generated")

    # 4. Create index (if not exists)
    create_index()
    print(f"Index '{INDEX_NAME}' ready")

    # 5. Store vectors in Endee
    store_vectors(embeddings, documents)
    print("Vectors stored successfully in Endee")


if __name__ == "__main__":
    main()
