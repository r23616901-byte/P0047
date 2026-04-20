# 🎓 AI-Based Lecture Summarizer

## Complete Audio-to-Text & Summarization System

A modern, hackathon-ready web application that converts lecture audio into structured smart notes using AI. Upload or record audio, get instant transcripts, summaries, and key points.

---

## ✨ Features

### Core Functionality
- **🎤 Audio Upload** - Drag & drop or browse to upload lecture files
- **🔴 Live Recording** - Record lectures directly in browser (Web Speech API)
- **📝 Full Transcription** - Convert speech to text using OpenAI Whisper
- **🧠 Smart Summarization** - AI-generated concise summaries
- **📌 Key Points Extraction** - Automatic extraction of important points

### User Experience
- **🎨 Modern UI** - Clean, professional interface
- **🌙 Dark Mode** - Toggle between light and dark themes
- **📱 Responsive** - Works on mobile, tablet, and desktop
- **🔍 Search** - Search within generated notes
- **📋 History** - Access previous summarizations
- **📥 Download** - Export notes as TXT files
- **📋 Copy** - Copy any section to clipboard

### Technical Features
- **Multiple Formats** - MP3, WAV, M4A, OGG, FLAC support
- **File Validation** - Size (50MB) and format checking
- **Error Handling** - Clear error messages
- **Loading States** - Visual feedback during processing
- **Live Transcript** - Real-time speech recognition preview

---

## 📁 Project Structure

```
project-root/
├── frontend/
│   ├── index.html          # Complete UI structure
│   ├── style.css           # Modern responsive styling
│   └── script.js           # All frontend logic
│
├── backend/
│   ├── app.py              # Flask + Whisper API server
│   ├── requirements.txt    # Python dependencies
│   ├── README.md           # Backend setup guide
│   ├── run.sh              # Quick start (macOS/Linux)
│   └── run.bat             # Quick start (Windows)
│
├── src/                    # React components (alternative frontend)
│   ├── App.tsx
│   └── components/
│
├── README.md               # This file
├── TESTING_GUIDE.md        # Complete testing scenarios
└── PROJECT_SUMMARY.md      # Quick reference
```

---

## 🚀 Quick Start Guide

### Prerequisites

1. **Node.js 18+** (for React frontend)
2. **Python 3.8+** (for backend)
3. **FFmpeg** (for audio processing)

### Step 1: Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### Step 2: Start Backend

```bash
cd backend

# macOS/Linux
chmod +x run.sh && ./run.sh

# Windows
run.bat
```

Backend runs on: `http://localhost:5000`

### Step 3: Open Frontend

**Option A: Vanilla HTML/CSS/JS (Recommended)**
```bash
# Simply open frontend/index.html in your browser
# Or use a local server:
cd frontend
python -m http.server 8080
# Open http://localhost:8080
```

**Option B: React Frontend**
```bash
npm install
npm run dev
# Open http://localhost:5173
```

---

## 🎯 User Flow

1. **Upload or Record** → Choose audio input method
2. **Click Summarize** → Process with AI
3. **View Results** → Transcript, Summary, Key Points
4. **Export** → Download or copy notes

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transcribe` | Audio → Transcript only |
| POST | `/summarize` | Audio → Transcript + Summary + Key Points |
| GET | `/health` | Server health check |
| GET | `/` | API information |

### Example API Response

```json
{
  "success": true,
  "transcript": "Full lecture text...",
  "summary": "Condensed summary...",
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "language": "en",
  "duration": 300.5
}
```

---

## 🎨 UI Components

### Input Section
- Tab navigation (Upload / Record)
- Drag & drop upload area
- File preview with remove option
- Recording controls with live transcript
- Audio preview player

### Output Section
- Tab navigation (Transcript / Summary / Key Points)
- Search bar with highlighting
- Word/point counters
- Copy, Download, New Session buttons

### Additional Features
- Dark mode toggle
- Toast notifications
- History panel
- Responsive design

---

## 🧪 Testing Scenarios

### ✅ Test Cases

1. **Upload Valid Audio** → Success with transcript
2. **Upload Invalid Format** → Error message
3. **Upload Large File (>50MB)** → Size error
4. **No File Upload** → Validation message
5. **Record Audio** → Working recording
6. **Live Transcript** → Real-time display
7. **Download Notes** → TXT file download
8. **Copy to Clipboard** → Success toast
9. **Dark Mode Toggle** → Theme switch
10. **Search in Notes** → Highlight matches

See `TESTING_GUIDE.md` for detailed test cases.

---

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Web Speech API (recording)
- MediaRecorder API (audio capture)
- Font Awesome (icons)
- Google Fonts (Inter)

### Backend
- Python 3.8+
- Flask (web framework)
- OpenAI Whisper (speech recognition)
- Flask-CORS (cross-origin support)

---

## 📝 Supported Audio Formats

| Format | Extension | Quality |
|--------|-----------|---------|
| MP3 | .mp3 | Good |
| WAV | .wav | Best |
| M4A | .m4a | Good |
| OGG | .ogg | Good |
| FLAC | .flac | Best |

---

## 🔐 Privacy & Security

- Files processed temporarily and deleted immediately
- No data stored on server
- Local browser storage for history only
- No external API calls (Whisper runs locally)

---

## 🚨 Troubleshooting

### Backend Issues

**FFmpeg not found:**
```bash
# Verify installation
ffmpeg -version

# Reinstall if needed
# Windows: winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

**Port 5000 in use:**
```python
# Change port in backend/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**Recording not working:**
- Allow microphone permissions in browser
- Use HTTPS or localhost
- Try Chrome/Edge (best support)

**API connection failed:**
- Ensure backend is running on port 5000
- Check CORS settings
- Verify API_BASE_URL in script.js

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Transcription Speed | ~1x real-time |
| File Size Limit | 50MB |
| Max History Items | 10 |
| Browser Support | Chrome, Edge, Firefox, Safari |

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] PDF export
- [ ] Speaker diarization
- [ ] Cloud storage
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] Timestamp-based navigation
- [ ] Video support

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 👥 Credits

- **OpenAI Whisper** - Speech recognition model
- **Flask** - Python web framework
- **Font Awesome** - Icons
- **Google Fonts** - Inter typeface

---

## 📞 Support

For issues or questions:
1. Check `TESTING_GUIDE.md`
2. Review console errors (F12)
3. Verify FFmpeg installation
4. Ensure backend is running

---

**Built with ❤️ for better learning**

*AI-Based Lecture Summarizer © 2026*
