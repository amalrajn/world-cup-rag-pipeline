"""
Setup Instructions for World Cup RAG System
============================================

Before running the system, you need to:

1. Setup:

$ git clone https://github.com/amalrajn/world-cup-rag-pipeline
$ cd world-cup-rag-pipeline

$ python -m venv .venv
# Linux or macOS
$ source .venv/bin/activate
# Windows
# .venv\Scripts\activate

$ pip install -r requirements.txt

2. Get a Google Gemini API Key:
   - Go to: https://aistudio.google.com/app/apikeys
   - Click "Create API Key"
   - Copy the key

3. Add the key to .env:
   - Open .env file in this directory
   - Replace: GOOGLE_API_KEY=your_api_key_here
   - With your actual key

3. Install dependencies:
   pip install -r requirements.txt

4. Run generation tests:
   python generation.py

5. Launch Gradio web interface:
   python app.py
   Then open: http://localhost:7860

Questions? Learn more about the pipeline design in planning.md

Video demo: https://www.loom.com/share/01451fcee01c4b23984a3a29f5990c5e
"""
