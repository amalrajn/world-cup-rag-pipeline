# World Cup RAG Pipeline

A lightweight Retrieval-Augmented Generation (RAG) demo for World Cup trivia and facts.

This repository includes document ingestion, retrieval, generation, and a simple Gradio interface to interact with the system.

## ✅ What’s included

- `scrape.py` — document scraping / content preparation
- `ingest.py` — build the vector store from the World Cup documents
- `retrieval.py` — search and retrieve relevant passages
- `generation.py` — run generation tests with the retrieval pipeline
- `app.py` — launch the Gradio web interface
- `documents/` — World Cup documents used for retrieval

## 🚀 Quick setup

```bash
git clone https://github.com/amalrajn/world-cup-rag-pipeline
cd world-cup-rag-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🔑 Configure API key

1. Create a Google Gemini API key at:
   `https://aistudio.google.com/app/apikeys`
2. Create a `.env` file in the project root if it does not exist.
3. Add this line:

```env
GOOGLE_API_KEY=your_api_key_here
```

## 🧪 Run the project

- Run generation checks:
  ```bash
  python generation.py
  ```

- Launch the Gradio app:
  ```bash
  python app.py
  ```

Open your browser at `http://localhost:7860`.

## 📚 Notes

- `planning.md` explains the pipeline design in more detail.
- The `documents/` directory contains all World Cup content used by the system.

## 🎥 Demo

Video demo: https://www.loom.com/share/01451fcee01c4b23984a3a29f5990c5e

