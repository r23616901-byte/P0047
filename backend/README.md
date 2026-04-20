# Backend - Audio to Text Module

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (required for Whisper audio processing)

### Installation

1. **Install FFmpeg** (required for audio processing):

   **Windows:**
   ```bash
   # Download from https://ffmpeg.org/download.html
   # Or use winget:
   winget install ffmpeg
   ```

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

2. **Create Virtual Environment** (recommended):
   ```bash
   cd backend
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server**:
   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5000`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/transcribe` | Transcribe audio to text |

### Testing the API

**Using curl:**
```bash
curl -X POST http://localhost:5000/transcribe \
  -F "audio=@/path/to/your/audio.mp3"
```

**Expected Response:**
```json
{
  "success": true,
  "transcript": "Your transcribed text here...",
  "language": "en",
  "duration": 120.5
}
```

### Supported Audio Formats
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)
- FLAC (.flac)

### Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Max File Size | 50MB | Maximum upload size |
| Whisper Model | base | Balance of speed & accuracy |
| Port | 5000 | Server port |

### Troubleshooting

**Error: "No module named whisper"**
```bash
pip install openai-whisper
```

**Error: "ffmpeg not found"**
- Install FFmpeg using the instructions above
- Ensure ffmpeg is in your system PATH

**Error: "CUDA out of memory" (GPU users)**
- Use a smaller model: change `whisper.load_model("base")` to `whisper.load_model("tiny")`
