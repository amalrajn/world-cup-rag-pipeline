"""
World Cup RAG System - Gradio Web Interface
===========================================

User-friendly query interface for the complete RAG pipeline.
Retrieves documents and generates grounded answers with source attribution.
"""

import gradio as gr
from generation import end_to_end_query, EmbeddingRetriever, GroundedGenerator
from retrieval import load_documents, FixedSizeChunker


# Global objects (initialized once)
_retriever = None
_generator = None


def initialize_pipeline():
    """Initialize retriever and generator on startup."""
    global _retriever, _generator
    
    if _retriever is None or _generator is None:
        # Set up retriever
        documents = load_documents("documents")
        chunker = FixedSizeChunker(chunk_size=900, overlap=150)
        chunked_docs = {}
        for filename, text in documents.items():
            chunks = chunker.chunk(text)
            chunked_docs[filename] = chunks
        
        _retriever = EmbeddingRetriever(embedding_model="all-MiniLM-L6-v2", top_k=5)
        _retriever.setup_vector_store(chunked_docs)
        
        # Set up generator
        _generator = GroundedGenerator(model_name="gemini-2.5-flash", temperature=0.3)


def ask_question(question: str) -> tuple[str, str, str]:
    """
    Process user question and return answer with sources.
    
    Parameters
    ----------
    question : str
        User's question about World Cup
    
    Returns
    -------
    tuple of (answer, sources, diagnostics)
    """
    if not question.strip():
        return "Please enter a question.", "", ""
    
    # Run pipeline
    result = end_to_end_query(question, _retriever, _generator)
    
    # Format sources
    sources_text = "\n".join(source for source in result["sources"])
    if not sources_text:
        sources_text = "No sources retrieved"
    
    # Format diagnostics
    scores = result["distance_scores"]
    distances_text = "\n".join(
        f"  • Chunk {i+1}: {score:.4f}" 
        for i, score in enumerate(scores)
    )
    
    # Calculate answer quality
    if scores:
        quality = 'High' if scores[0] < 0.35 else 'Medium' if scores[0] < 0.5 else 'Low'
    else:
        quality = 'Unknown'
    
    diagnostics = f"""Retrieval Quality:
{distances_text}

Answer Quality: {quality}
Grounded: {'Yes' if result['sources'] else 'No sources'}"""
    
    return result["answer"], sources_text, diagnostics


def main():
    """Build and launch Gradio interface."""
    
    # Initialize on startup
    initialize_pipeline()
    
    # Build interface
    with gr.Blocks(title="World Cup Q&A System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
# World Cup RAG System
**Retrieval-Augmented Generation for World Cup Questions**

Ask questions about World Cup records, history, facts, and trivia. 
The system will search through documents and provide grounded answers with sources.
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="e.g., 'Who has scored the most goals in World Cup history?'",
                    lines=2
                )
                ask_btn = gr.Button("Ask", scale=1)
            
        with gr.Row():
            with gr.Column(scale=2):
                answer_output = gr.Textbox(
                    label="Answer",
                    lines=8,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                sources_output = gr.Textbox(
                    label="Retrieved Sources",
                    lines=8,
                    interactive=False
                )
                diagnostics_output = gr.Textbox(
                    label="Diagnostics",
                    lines=6,
                    interactive=False
                )
        
        # Example questions
        gr.Markdown("### Example Questions")
        with gr.Row():
            examples = [
                ["Who has scored the most goals in World Cup history?"],
                ["Which country hosted the 2022 World Cup?"],
                ["Who scored a hat-trick in a World Cup final?"],
                ["What are the oldest and youngest goal scorers in World Cup history?"],
            ]
            
            for example in examples[:2]:
                gr.Button(example[0], size="sm").click(
                    lambda q=example[0]: (q, *ask_question(q)),
                    inputs=[],
                    outputs=[question_input, answer_output, sources_output, diagnostics_output]
                )
            
            for example in examples[2:]:
                gr.Button(example[0], size="sm").click(
                    lambda q=example[0]: (q, *ask_question(q)),
                    inputs=[],
                    outputs=[question_input, answer_output, sources_output, diagnostics_output]
                )
        
        # Bind click and submit events
        ask_btn.click(
            ask_question,
            inputs=question_input,
            outputs=[answer_output, sources_output, diagnostics_output]
        )
        
        question_input.submit(
            ask_question,
            inputs=question_input,
            outputs=[answer_output, sources_output, diagnostics_output]
        )
        
        gr.Markdown("""
---
### About This System

This is a **Retrieval-Augmented Generation (RAG)** system that:
1. **Retrieves** relevant documents using semantic search (all-MiniLM-L6-v2 embeddings)
2. **Grounds** answers in retrieved context using Gemini Flash Lite
3. **Attributes** sources automatically for transparency

The system only uses information from provided World Cup documents. 
If a question can't be answered from the available documents, the system will say so explicitly.
        """)
    
    # Launch
    demo.launch(
        server_name="0.0.0.0",
        server_port=3000,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
