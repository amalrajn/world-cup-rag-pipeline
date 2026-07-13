"""Pre-build the ChromaDB vector store at image-build time.

Running this during `docker build` bakes the embedded store (and the ONNX
embedding model) into the image, so the container starts and binds its port
immediately instead of embedding hundreds of chunks on every cold start.

The chunking parameters here MUST match initialize_pipeline() in app.py so the
runtime reuses the pre-built collection instead of rebuilding it.
"""
from ingest import load_documents, FixedSizeChunker
from retrieval import EmbeddingRetriever


def main():
    documents = load_documents("documents")
    chunker = FixedSizeChunker(chunk_size=900, overlap=150)
    chunked_docs = {name: chunker.chunk(text) for name, text in documents.items()}

    retriever = EmbeddingRetriever(embedding_model="all-MiniLM-L6-v2", top_k=5)
    retriever.setup_vector_store(chunked_docs)


if __name__ == "__main__":
    main()
