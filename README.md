# AI-Based Lecture Summarizer

## Task 1: Audio to Text Module

A web application that converts lecture audio files into text transcripts using OpenAI's Whisper speech recognition model.

---

## 🎯 Features

- **Audio Upload**: Drag & drop or click to upload audio files
- **Multiple Formats**: Supports MP3, WAV, M4A, OGG, FLAC
- **AI Transcription**: Powered by OpenAI Whisper
- **Clean UI**: Modern, responsive interface
- **Export Options**: Copy or download transcripts
- **File Validation**: Size and format checking

---

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── app.py              # Flask server with Whisper integration
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend setup instructions
│
├── src/
│   ├── components/
│   │   ├── AudioUploader.tsx    # File upload component
│   │   ├── FilePreview.tsx      # Selected file display
│   │   └── TranscriptDisplay.tsx # Transcript output
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # React entry point
│   └── index.css           # Global styles
│
├── index.html              # HTML template
├── package.json            # Node.js dependencies
├── vite.config.ts          # Vite configuration
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.8+ (for backend)
- **FFmpeg** (for audio processing)

---

### Step 1: Install FFmpeg

FFmpeg is required for Whisper to process audio files.

**Windows:**
```bash
winget install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

---

### Step 2: Setup Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

The backend will start on `http://localhost:5000`

---

### Step 3: Setup Frontend

Open a **new terminal** (keep backend running):

```bash
# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:5173` (or similar port)

---

### Step 4: Test the Application

1. Open your browser and go to the frontend URL (e.g., `http://localhost:5173`)
2. Upload an audio file (MP3, WAV, M4A, etc.)
3. Click "Convert to Text"
4. Wait for the transcription to complete
5. View, copy, or download the transcript

---

## 📡 API Reference

### POST /transcribe

Transcribe an audio file to text.

**Request:**
```
Content-Type: multipart/form-data

Form Fields:
- audio: [Audio File]
```

**Response (Success):**
```json
{
  "success": true,
  "transcript": "Full lecture text...",
  "language": "en",
  "duration": 120.5
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message here"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model": "whisper-base",
  "timestamp": "2026-01-15T10:30:00"
}
```

---

## ⚙️ Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Backend Port | 5000 | Flask server port |
| Frontend Port | 5173 | Vite dev server port |
| Max File Size | 50MB | Maximum upload size |
| Whisper Model | base | Speed/accuracy balance |

---

## 🎵 Supported Audio Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| MP3 | .mp3 | Most common audio format |
| WAV | .wav | Uncompressed audio |
| M4A | .m4a | Apple audio format |
| OGG | .ogg | Open source format |
| FLAC | .flac | Lossless audio |

---

## 🧪 Testing

### Test Case 1: Valid Audio File
1. Upload a valid MP3 file
2. Click "Convert to Text"
3. **Expected**: Transcript displayed successfully

### Test Case 2: Invalid File Format
1. Try to upload a .txt or .pdf file
2. **Expected**: Error message about unsupported format

### Test Case 3: No Backend Connection
1. Stop the backend server
2. Try to convert an audio file
3. **Expected**: Error message about server connection

### Test Case 4: Large File
1. Upload a file larger than 50MB
2. **Expected**: Error message about file size limit

---

## 🔧 Troubleshooting

### "Cannot connect to backend server"
- Ensure backend is running: `python app.py` in `backend/` folder
- Check that port 5000 is not blocked by firewall
- Verify no other application is using port 5000

### "ffmpeg not found"
- Install FFmpeg using the instructions above
- Restart your terminal after installation
- Verify installation: `ffmpeg -version`

### "No module named whisper"
- Activate the virtual environment
- Run: `pip install -r requirements.txt`

### "CUDA out of memory" (GPU users)
- Edit `backend/app.py`
- Change `whisper.load_model("base")` to `whisper.load_model("tiny")`

---

## 📝 Notes

- First transcription may take longer as Whisper model loads
- Processing time depends on audio length and system specs
- Transcripts are not saved on the server (privacy-focused)
- For production, add authentication and storage

---

## 🔮 Next Steps (Future Tasks)

- **Task 2**: Text Summarization (NLP)
- **Task 3**: Key Points Extraction
- **Task 4**: User Authentication
- **Task 5**: Transcript History & Storage

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

AI-Based Lecture Summarizer Project
Task 1: Audio to Text Module
