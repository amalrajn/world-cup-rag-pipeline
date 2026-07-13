"""
Retrieval Stage - Embedding & Vector Store
==========================================

Embeds chunks using all-MiniLM-L6-v2 and stores them in ChromaDB.
Provides retrieval function to find top-k relevant chunks for a query.
"""

import os
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, FixedSizeChunker


class EmbeddingRetriever:
    """
    Manages embedding and retrieval of chunks using ChromaDB and SentenceTransformer.
    Uses persistent storage to avoid re-embedding on each startup.
    
    Parameters
    ----------
    embedding_model : str
        Name of the embedding model (default: all-MiniLM-L6-v2)
    top_k : int
        Number of chunks to retrieve per query (default: 5)
    persist_dir : str
        Directory for persistent ChromaDB storage (default: .chroma_db)
    """

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", top_k: int = 5, persist_dir: str = ".chroma_db"):
        self.embedding_model_name = embedding_model
        self.top_k = top_k
        self.persist_dir = persist_dir
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model}...")
        self.embedder = SentenceTransformer(embedding_model)
        print("Model loaded\n")

        # Initialize ChromaDB with persistent storage
        os.makedirs(persist_dir, exist_ok=True)
        print(f"Connecting to ChromaDB at {persist_dir}...")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = None

    def setup_vector_store(self, chunked_docs: dict) -> None:
        """
        Embed chunks and store them in ChromaDB with metadata.
        Reuses existing collection if already embedded (persistent storage).
        
        Parameters
        ----------
        chunked_docs : dict
            Dictionary mapping filenames to lists of chunks from ingest.py
        """
        print("Setting up vector store...")

        # Expected chunk count for the current document set. Used to decide
        # whether a persisted collection is still in sync with documents/.
        expected_count = sum(len(chunks) for chunks in chunked_docs.values())

        # Try to reuse existing collection (fast if already embedded), but only
        # if it matches the current documents. If documents were added/removed,
        # the persisted store would otherwise serve stale chunks from deleted
        # files, so we rebuild it instead.
        existing_collections = self.client.list_collections()
        collection_names = [c.name for c in existing_collections]

        if "world_cup_chunks" in collection_names:
            existing = self.client.get_collection(name="world_cup_chunks")
            existing_count = existing.count()

            if existing_count == expected_count:
                print("  Reusing existing collection...")
                self.collection = existing
                print(f"Loaded existing collection with {existing_count} chunks\n")
                return

            print(
                f"  Documents changed (store has {existing_count} chunks, "
                f"current docs produce {expected_count}); rebuilding..."
            )
            self.client.delete_collection(name="world_cup_chunks")

        # Create new collection
        print("  Creating new collection...")
        self.collection = self.client.create_collection(
            name="world_cup_chunks",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Collect all chunks
        all_chunks = []
        all_ids = []
        all_metadata = []
        chunk_id = 0
        
        for filename, chunks in chunked_docs.items():
            for chunk in chunks:
                chunk_id += 1
                all_chunks.append(chunk["text"])
                all_ids.append(f"chunk_{chunk_id}")
                all_metadata.append({
                    "source": filename,
                    "chunk_index": chunk["index"],
                    "start_char": chunk["start_char"],
                })
        
        # Add chunks to collection in batches
        print(f"  Embedding and storing {len(all_chunks)} chunks...")
        batch_size = 50
        for i in range(0, len(all_chunks), batch_size):
            batch_end = min(i + batch_size, len(all_chunks))
            self.collection.add(
                ids=all_ids[i:batch_end],
                documents=all_chunks[i:batch_end],
                metadatas=all_metadata[i:batch_end],
            )
        
        print(f"Embedded and stored {len(all_chunks)} chunks in ChromaDB\n")

    def retrieve(self, query: str, k: int = None) -> list[dict]:
        """
        Retrieve top-k most relevant chunks for a query using ChromaDB.
        
        Parameters
        ----------
        query : str
            The search query
        k : int, optional
            Number of results to return (uses self.top_k if not specified)
        
        Returns
        -------
        list[dict]
            List of dicts with keys: text, source, chunk_index, distance
        """
        if k is None:
            k = self.top_k
        
        if self.collection is None:
            raise ValueError("Vector store not initialized. Call setup_vector_store() first.")
        
        # Query the collection
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
        )
        
        # Format results
        retrieved_chunks = []
        if results and results["documents"] and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                
                retrieved_chunks.append({
                    "text": doc,
                    "source": metadata["source"],
                    "chunk_index": metadata["chunk_index"],
                    "distance": distance,
                })
        
        return retrieved_chunks

    def __repr__(self):
        return (f"EmbeddingRetriever(model={self.embedding_model_name}, "
                f"top_k={self.top_k})")


def print_retrieval_results(query: str, results: list[dict], query_num: int = None) -> None:
    """
    Pretty-print retrieval results for analysis.
    """
    header = f"QUERY #{query_num}" if query_num else "QUERY"
    print("\n" + "=" * 80)
    print(header)
    print("=" * 80)
    print(f"\n{query}\n")

    if not results:
        print("No results found\n")
        return
    
    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result #{i} ---")
        print(f"Source: {chunk['source']}")
        print(f"Chunk Index: {chunk['chunk_index']}")
        print(f"Distance Score: {chunk['distance']:.4f}")
        
        # Assess score quality
        if chunk['distance'] < 0.3:
            assessment = "Excellent match"
        elif chunk['distance'] < 0.5:
            assessment = "Good match"
        elif chunk['distance'] < 0.7:
            assessment = "Moderate match"
        else:
            assessment = "Weak match"
        
        print(f"Assessment: {assessment}")
        print(f"\nContent:\n{chunk['text']}\n")


def main():
    """Main retrieval pipeline: load, embed, test retrieval."""
    
    print("=" * 80)
    print("WORLD CUP RAG SYSTEM - EMBEDDING & RETRIEVAL")
    print("=" * 80 + "\n")
    
    # Load and chunk documents
    print("Loading documents...")
    documents = load_documents("documents")
    print(f"Loaded {len(documents)} documents\n")

    print("Chunking documents...")
    chunker = FixedSizeChunker(chunk_size=900, overlap=150)
    chunked_docs = {}
    total_chunks = 0
    for filename, text in documents.items():
        chunks = chunker.chunk(text)
        chunked_docs[filename] = chunks
        total_chunks += len(chunks)
    print(f"Created {total_chunks} chunks\n")
    
    # Set up retriever and embed chunks
    retriever = EmbeddingRetriever(embedding_model="all-MiniLM-L6-v2", top_k=5)
    print(f"Using: {retriever}\n")
    
    retriever.setup_vector_store(chunked_docs)
    
    # Test retrieval with evaluation queries
    print("=" * 80)
    print("RETRIEVAL TESTING")
    print("=" * 80)
    
    test_queries = [
        ("Who has scored the most goals in World Cup history?", "Miroslav Klose"),
        ("Which country was the winner of the tenth edition of the World Cup?", "West Germany"),
        ("Who scored a hat-trick in a world cup final and lost?", "Kylian Mbappé"),
        ("Which stadium was the 2010 World Cup Final held in?", "Soccer City Stadium"),
        ("Where was the 1990 World Cup held?", "Italy"),
    ]
    
    # Test with first 3 queries
    for i, (query, expected_answer) in enumerate(test_queries[:3], 1):
        results = retriever.retrieve(query, k=5)
        print_retrieval_results(query, results, query_num=i)
        print(f"Expected answer: {expected_answer}")
    
    # Retrieval quality summary
    print("\n" + "=" * 80)
    print("RETRIEVAL QUALITY ASSESSMENT")
    print("=" * 80)
    
    print("\nRetrieval tests completed")
    print("\nChecklist:")
    print("  [ ] Retrieved chunks visibly relate to each query")
    print("  [ ] Distance scores on top results are below 0.5")
    print("  [ ] Source metadata is correct")
    print("  [ ] No leftover HTML or boilerplate in chunks")
    print("\nIf any of these don't check out, debug:")
    print("  - Print full chunk content above")
    print("  - Check distance scores (>0.6 = weak match)")
    print("  - Verify metadata is correctly stored")
    print("  - Consider adjusting chunk size or overlap")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
