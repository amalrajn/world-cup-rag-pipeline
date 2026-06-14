"""
Setup Instructions for World Cup RAG System
============================================

Before running the system, you need to:

1. Get a Google Gemini API Key:
   - Go to: https://aistudio.google.com/app/apikeys
   - Click "Create API Key"
   - Copy the key

2. Add the key to .env:
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
"""
