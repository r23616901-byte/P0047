# 🚀 AI Lecture Summarizer - Quick Start Guide

## Get Running in 5 Minutes!

---

## ⚡ Ultra-Fast Setup

### Step 1: Install FFmpeg (Required)

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

✅ Verify: `ffmpeg -version`

---

### Step 2: Start Backend (Terminal 1)

```bash
cd backend

# macOS/Linux
chmod +x run.sh && ./run.sh

# Windows
run.bat
```

**Expected Output:**
```
============================================================
AI-Based Lecture Summarizer - Audio to Text Server
============================================================
Loading Whisper model...
✅ Model loaded successfully!
Supported formats: mp3, wav, m4a, ogg, flac
Max file size: 50MB
============================================================
 * Running on http://0.0.0.0:5000
```

✅ Backend running on: `http://localhost:5000`

---

### Step 3: Open Frontend (Browser)

**Option A: Direct File (Easiest)**
```
Simply open: frontend/index.html in your browser
```

**Option B: Local Server**
```bash
cd frontend
python -m http.server 8080
```
Then open: `http://localhost:8080`

---

## 🎯 You're Ready!

Your AI Lecture Summarizer is now running!

### Test It:
1. Upload an audio file (MP3/WAV)
2. Click "Summarize Lecture"
3. Wait for processing
4. View Transcript, Summary, and Key Points

---

## 📱 Alternative: React Frontend

If you prefer React:

```bash
# In project root
npm install
npm run dev
```

Open: `http://localhost:5173`

---

## 🧪 Quick Test

### Test Upload:
1. Go to frontend (port 8080 or file)
2. Click upload area
3. Select any audio file
4. Click "Summarize"
5. See results!

### Test Recording:
1. Click "Record Audio" tab
2. Click "Start Recording"
3. Allow microphone
4. Speak for 10 seconds
5. Click "Stop Recording"
6. Click "Summarize"

---

## 🔧 Troubleshooting

### "FFmpeg not found"
```bash
# Reinstall FFmpeg
# Windows: winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### "Backend not responding"
- Check if backend is running
- Verify port 5000 is not in use
- Check console for errors

### "Recording not working"
- Allow microphone permissions
- Use Chrome or Edge browser
- Ensure using HTTPS or localhost

### "File too large"
- Maximum file size: 50MB
- Compress audio or split into parts

---

## 📊 What You Get

### Input Options:
- 📤 Upload audio files (MP3, WAV, M4A, OGG, FLAC)
- 🎤 Record directly in browser

### Output:
- 📝 Full transcript
- 🧠 Concise summary
- 📌 Key points (bullet list)

### Features:
- 🌙 Dark mode
- 🔍 Search in notes
- 📋 Copy to clipboard
- 📥 Download as TXT
- 📜 History of past summaries

---

## 🎨 UI Preview

```
┌─────────────────────────────────────────┐
│  🌙  AI Lecture Summarizer              │
│      Convert lectures into smart notes  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 📤 Input Audio                     │ │
│  │ [Upload File] [Record Audio]      │ │
│  │                                   │ │
│  │   Drag & Drop or Click to Upload  │ │
│  │                                   │ │
│  │      [✨ Summarize Lecture]      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 📄 Lecture Notes   [Copy][Download]│ │
│  │ 🔍 Search...                       │ │
│  │ ─────────────────────────────────  │ │
│  │ [Transcript][Summary][Key Points] │ │
│  │                                   │ │
│  │ Your results appear here...       │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 📁 Project Files

```
project/
├── frontend/
│   ├── index.html      ← Open this in browser
│   ├── style.css       ← All styling
│   └── script.js       ← All logic
│
├── backend/
│   ├── app.py          ← Flask server
│   ├── requirements.txt
│   └── run.sh / run.bat
│
└── Documentation/
    ├── README_COMPLETE.md
    ├── TESTING_GUIDE.md
    ├── PROJECT_SUMMARY.md
    └── QUICK_START.md   ← You are here
```

---

## 🎯 Demo Checklist

Before presenting to judges:

- [ ] Backend running (port 5000)
- [ ] Frontend open in browser
- [ ] Test audio file ready
- [ ] Microphone working
- [ ] Dark mode tested
- [ ] Download feature tested
- [ ] No console errors (F12)

---

## 📞 Need Help?

1. **Check Documentation:**
   - `README_COMPLETE.md` - Full docs
   - `TESTING_GUIDE.md` - Test scenarios
   - `PROJECT_SUMMARY.md` - Quick reference

2. **Common Issues:**
   - FFmpeg not installed
   - Port already in use
   - Microphone permissions denied

3. **Verify Setup:**
   ```bash
   # Check FFmpeg
   ffmpeg -version
   
   # Check Python
   python --version
   
   # Check backend
   curl http://localhost:5000/health
   ```

---

## 🏆 Success Indicators

✅ Backend starts without errors  
✅ Frontend loads in browser  
✅ File upload works  
✅ Summarization produces output  
✅ All 3 tabs show content  
✅ Dark mode toggles  
✅ Download creates file  
✅ No console errors  

---

## 🎓 Ready for Your Demo!

You now have a fully functional AI Lecture Summarizer with:

✨ Modern, professional UI  
✨ Audio upload and recording  
✨ AI-powered transcription  
✨ Smart summarization  
✨ Key point extraction  
✨ Search, copy, download  
✨ Dark mode  
✨ History tracking  

**Good luck with your presentation! 🚀**

---

**AI-Based Lecture Summarizer © 2026**  
*Built for students, powered by AI*
