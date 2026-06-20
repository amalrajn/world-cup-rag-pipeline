"""
Document Ingestion and Chunking Pipeline
=========================================

Loads documents from the documents/ folder and splits them into chunks
using a fixed-size chunking strategy with configurable overlap.
"""

import os
import glob
from pathlib import Path

# Document sources (synced with scrape.py SOURCES)
SOURCE_NAMES = {
    "FIFA_World_Cup_records_and_statistics.txt",
    "History_of_the_FIFA_World_Cup.txt",
    "FIFA_World_Cup.txt",
    "List_of_FIFA_World_Cup_hosts.txt",
    "List_of_FIFA_World_Cup_songs_and_anthems.txt",
    "List_of_FIFA_World_Cup_finals.txt",
    "Economics_of_the_FIFA_World_Cup.txt",
    "2026_FIFA_World_Cup_qualification.txt",
    "National_team_appearances_in_the_FIFA_World_Cup.txt",
    "List_of_FIFA_World_Cup_hattricks.txt",
}


class FixedSizeChunker:
    """
    Splits text by character count with configurable size and overlap.

    Parameters
    ----------
    chunk_size : int
        Number of characters per chunk. Default: 500.
    overlap : int
        Number of characters to repeat at the start of the next chunk.
        Overlap helps avoid cutting off context at chunk boundaries.
        Default: 50.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[dict]:
        """
        Split text into fixed-size chunks.

        Returns a list of dicts with keys:
            - text: the chunk content
            - index: position of this chunk in the document
            - start_char: character offset where this chunk begins
            - strategy: always "fixed_size"
        """
        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "index": index,
                "start_char": start,
                "strategy": "fixed_size",
            })

            # Advance by chunk_size minus overlap so the next chunk
            # starts slightly before the end of this one
            start += self.chunk_size - self.overlap
            index += 1

        return chunks

    def __repr__(self):
        return f"FixedSizeChunker(chunk_size={self.chunk_size}, overlap={self.overlap})"


def load_documents(folder: str = "documents") -> dict:
    """
    Load only whitelisted .txt files from the documents folder.
    
    Only documents in SOURCE_NAMES are loaded to ensure consistency
    with the scrape.py SOURCES list.

    Returns
    -------
    dict
        Dictionary mapping filenames to text content.
    """
    documents = {}
    txt_files = glob.glob(os.path.join(folder, "*.txt"))

    for filepath in sorted(txt_files):
        filename = os.path.basename(filepath)
        
        # Only load documents that are in our SOURCE_NAMES whitelist
        if filename not in SOURCE_NAMES:
            print(f"⊘ Skipped (not in SOURCE_NAMES): {filename}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                documents[filename] = f.read()
            print(f"✓ Loaded: {filename} ({len(documents[filename])} characters)")
        except Exception as e:
            print(f"✗ Failed to load {filename}: {e}")

    return documents


def chunk_documents(documents: dict, chunker: FixedSizeChunker) -> dict:
    """
    Chunk all documents using the provided chunker.

    Returns
    -------
    dict
        Dictionary mapping filenames to lists of chunks.
    """
    chunked = {}
    total_chunks = 0

    for filename, text in documents.items():
        chunks = chunker.chunk(text)
        chunked[filename] = chunks
        total_chunks += len(chunks)
        print(f"  → {len(chunks)} chunks from {filename}")

    return chunked, total_chunks


def inspect_chunks(chunked_docs: dict, num_samples: int = 5) -> None:
    """
    Print representative chunks for quality inspection.

    Shows:
    - Does this chunk make sense on its own?
    - Is it complete or fragmented?
    - Any leftover HTML or boilerplate?
    """
    print("\n" + "=" * 80)
    print("CHUNK QUALITY INSPECTION")
    print("=" * 80)
    print(f"\nShowing {num_samples} representative chunks across documents:\n")

    chunk_count = 0
    for filename, chunks in chunked_docs.items():
        if not chunks or chunk_count >= num_samples:
            continue

        # Show first, middle, and last chunks from this document
        samples = []
        if len(chunks) >= 3:
            samples = [chunks[0], chunks[len(chunks) // 2], chunks[-1]]
        else:
            samples = chunks[:num_samples - chunk_count]

        for chunk in samples:
            if chunk_count >= num_samples:
                break

            chunk_count += 1
            text = chunk["text"]

            # Check for quality issues
            issues = []
            if len(text.split()) < 5:
                issues.append("❌ Too small/fragmented")
            if text.endswith('-') or text[-1:].isalpha() == False and text[-1:] not in '.!?,;:':
                issues.append("⚠️  May be mid-word")
            if '&' in text or '<' in text or '[' in text:
                issues.append("⚠️  Possible HTML artifact")

            print(f"\n--- Chunk #{chunk_count} from {filename} ---")
            print(f"Index: {chunk['index']}, Start char: {chunk['start_char']}")
            print(f"Length: {len(text)} chars, {len(text.split())} words")
            if issues:
                print(f"Issues: {', '.join(issues)}")
            print(f"\nContent:\n{text[:200]}{'...' if len(text) > 200 else ''}\n")


def print_full_chunks(chunked_docs: dict, num_chunks: int = 5) -> None:
    """
    Print the full text of 5 representative chunks for detailed review.
    """
    print("\n" + "=" * 80)
    print("FULL CHUNK SAMPLES")
    print("=" * 80)
    print(f"\nShowing {num_chunks} complete chunks:\n")

    chunk_count = 0
    for filename, chunks in chunked_docs.items():
        if not chunks or chunk_count >= num_chunks:
            continue

        # Select diverse chunks: first, middle, last
        indices = []
        if len(chunks) >= 3:
            indices = [0, len(chunks) // 2, len(chunks) - 1]
        else:
            indices = list(range(len(chunks)))

        for idx in indices:
            if chunk_count >= num_chunks:
                break

            chunk = chunks[idx]
            chunk_count += 1

            print(f"\n{'─' * 80}")
            print(f"CHUNK {chunk_count} | From: {filename} | Index: {chunk['index']}")
            print(f"{'─' * 80}")
            print(f"{chunk['text']}")
            print()


def main():
    """Main pipeline: load, chunk, and inspect documents."""

    print("=" * 80)
    print("WORLD CUP RAG SYSTEM - DOCUMENT INGESTION & CHUNKING")
    print("=" * 80 + "\n")

    # Load documents
    print("📄 Loading documents...")
    documents = load_documents("documents")
    print(f"✓ Loaded {len(documents)} documents\n")

    if not documents:
        print("❌ No documents found. Ensure documents/ folder contains .txt files")
        return

    # Configure chunker
    # User specified: 50 words with 10 token overlap
    # Adjusted to smaller chunks for better retrieval precision
    # 40 words ≈ 250 characters (average 6 chars/word + space)
    # 8 tokens ≈ 50 characters overlap
    chunk_size = 900
    overlap = 150

    print(f"   Chunk size: {chunk_size} characters (~40 words)")
    print(f"   Overlap: {overlap} characters (~8 tokens)\n")

    chunker = FixedSizeChunker(chunk_size=chunk_size, overlap=overlap)
    print(f"   Using: {chunker}\n")

    # Chunk all documents
    print("Chunking documents...")
    chunked_docs, total_chunks = chunk_documents(documents, chunker)
    print(f"\n✓ Total chunks created: {total_chunks}\n")

    # Inspect chunks
    inspect_chunks(chunked_docs, num_samples=5)

    # Print full chunks
    print_full_chunks(chunked_docs, num_chunks=5)

    # Analysis
    print("\n" + "=" * 80)
    print("CHUNKING ANALYSIS")
    print("=" * 80)
    print(f"\nTotal documents: {len(documents)}")
    print(f"Total chunks: {total_chunks}")
    print(f"Average chunks per document: {total_chunks / len(documents):.1f}")


    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
