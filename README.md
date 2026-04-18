# AI-Based Lecture Summarizer

A full-stack prototype application that takes an audio file (lecture), transcribes the speech to text, and uses NLP to generate a concise summary and key highlights.

## Tech Stack
- **Frontend**: Vanilla HTML5, CSS (Premium Glassmorphism Design), JavaScript
- **Backend**: Python FastAPI
- **AI Models**: `SpeechRecognition` (Google Web Speech) and HuggingFace Transformers (`sshleifer/distilbart-cnn-12-6`)

## Setup Instructions

### 1. Backend Setup
Make sure you have Python installed on your system. Navigate to the `backend` folder and install the AI requirements:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the AI Server
Start the FastAPI server:
```bash
python main.py
```
> **Note:** On the very first run, the open-source NLP summarization model will be downloaded to your machine. This might take a few minutes depending on your internet connection!

### 3. Frontend Setup
Simply double-click the `frontend/index.html` file to open it in Google Chrome or your preferred web browser. Or, right-click and use an extension like VSCode LiveServer.

## Usage
- Drag and drop a `.wav` or `.mp3` audio file into the web UI.
- Click **"Generate Summary"**.
- Wait for the server to process the transcript and NLP summary.
- The results will be neatly laid out in structured tabs!
