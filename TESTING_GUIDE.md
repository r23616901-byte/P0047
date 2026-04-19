# Testing Guide - Audio to Text Module

## Quick Test Run

### 1. Start Backend Server

**Option A: Using Script (Recommended)**

macOS/Linux:
```bash
cd backend
chmod +x run.sh
./run.sh
```

Windows:
```cmd
cd backend
run.bat
```

**Option B: Manual Setup**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

You should see:
```
============================================================
AI-Based Lecture Summarizer - Audio to Text Server
============================================================
Supported formats: mp3, wav, m4a, ogg, flac
Max file size: 50MB
============================================================
 * Running on http://0.0.0.0:5000
```

### 2. Start Frontend

Open a **new terminal**:
```bash
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### 3. Test in Browser

1. Open `http://localhost:5173` in your browser
2. You should see the AI-Based Lecture Summarizer interface

---

## Test Scenarios

### ✅ Test 1: Successful Transcription

**Steps:**
1. Prepare a short audio file (MP3 or WAV, 1-2 minutes)
2. Click or drag the file to the upload area
3. Verify file name appears in the preview
4. Click "Convert to Text"
5. Wait for processing (loading spinner appears)
6. Verify transcript appears in the output box

**Expected Result:**
- ✅ File uploads successfully
- ✅ Loading indicator shows during processing
- ✅ Transcript displays after completion
- ✅ Language and duration shown (if available)

---

### ✅ Test 2: File Format Validation

**Steps:**
1. Try to upload a `.txt` or `.pdf` file
2. Observe the error message

**Expected Result:**
- ✅ Error message: "Unsupported file format"
- ✅ Allowed formats listed: mp3, wav, m4a, ogg, flac

---

### ✅ Test 3: File Size Validation

**Steps:**
1. Try to upload a file larger than 50MB
2. Observe the error message

**Expected Result:**
- ✅ Error message: "File too large. Maximum size is 50MB"

---

### ✅ Test 4: No File Submission

**Steps:**
1. Don't upload any file
2. The convert button should be disabled or show a message

**Expected Result:**
- ✅ Convert button is disabled until file is uploaded
- ✅ Or shows message: "Please select an audio file first"

---

### ✅ Test 5: Backend Connection Error

**Steps:**
1. Stop the backend server (Ctrl+C)
2. Try to convert an audio file from the frontend
3. Observe the error message

**Expected Result:**
- ✅ Error message about server connection
- ✅ Helpful message: "Cannot connect to backend server"

---

### ✅ Test 6: Copy Transcript

**Steps:**
1. Successfully transcribe an audio file
2. Click the "Copy" button
3. Paste into a text editor

**Expected Result:**
- ✅ Transcript copied to clipboard
- ✅ Success message appears

---

### ✅ Test 7: Download Transcript

**Steps:**
1. Successfully transcribe an audio file
2. Click the "Download" button
3. Check downloads folder

**Expected Result:**
- ✅ TXT file downloaded
- ✅ Filename format: `transcript-YYYY-MM-DD.txt`
- ✅ File contains the full transcript

---

### ✅ Test 8: Remove File

**Steps:**
1. Upload an audio file
2. Click the X (remove) button on the file preview
3. Verify the file is removed

**Expected Result:**
- ✅ File preview disappears
- ✅ Upload area is ready for new file
- ✅ Convert button is disabled

---

### ✅ Test 9: Multiple Conversions

**Steps:**
1. Transcribe first audio file
2. Remove the file
3. Upload a different audio file
4. Transcribe again

**Expected Result:**
- ✅ Second transcription works correctly
- ✅ Previous transcript is replaced
- ✅ No errors or conflicts

---

### ✅ Test 10: API Health Check

**Steps:**
1. With backend running, open browser
2. Go to: `http://localhost:5000/health`
3. Check the response

**Expected Result:**
```json
{
  "status": "healthy",
  "model": "whisper-base",
  "timestamp": "2026-01-15T10:30:00"
}
```

---

## Sample Test Audio

If you don't have test audio files, you can:

### Option 1: Record Your Own
- Use your phone or computer to record a short voice memo
- Save as MP3 or WAV
- Keep it under 50MB

### Option 2: Download Sample Audio
- Find free sample audio files online
- Ensure they are in supported formats (MP3, WAV, M4A, OGG, FLAC)

### Option 3: Use Online Test Files
- Search for "sample MP3 file" or "test audio WAV"
- Many websites provide free sample audio files

---

## Performance Expectations

| Audio Length | Processing Time (approx) |
|--------------|-------------------------|
| 1 minute     | 10-20 seconds           |
| 5 minutes    | 1-2 minutes             |
| 10 minutes   | 2-4 minutes             |
| 30 minutes   | 5-10 minutes            |

*Times vary based on system specs and model size*

---

## Common Issues & Solutions

### Issue: "Module not found: whisper"
**Solution:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "FFmpeg not found"
**Solution:**
- Install FFmpeg (see README.md)
- Restart terminal after installation
- Verify: `ffmpeg -version`

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Find and kill the process using port 5000
# macOS/Linux:
lsof -i :5000
kill -9 <PID>

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Slow transcription
**Solution:**
- Use smaller Whisper model in `app.py`:
  ```python
  model = whisper.load_model("tiny")  # Faster, less accurate
  ```

---

## Success Criteria

✅ All 10 test scenarios pass
✅ No console errors in browser
✅ No errors in backend terminal
✅ Transcript is accurate and readable
✅ UI is responsive and user-friendly
✅ Error messages are clear and helpful

---

## Next Steps After Testing

1. ✅ All tests pass → Ready for Task 2 (Summarization)
2. ⚠️ Some tests fail → Review error messages and fix issues
3. ❌ Major issues → Check backend logs and browser console

---

**Happy Testing! 🎉**
