# 🧪 AI Lecture Summarizer - Complete Testing Guide

## Testing Checklist for Judges/Demo

---

## 📋 Pre-Testing Setup

### ✅ Prerequisites Check

- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] Backend running (`http://localhost:5000`)
- [ ] Frontend open in browser
- [ ] Microphone permissions granted
- [ ] Test audio files ready

---

## 🎯 Test Scenarios (10 Critical Tests)

### Test 1: Upload Valid Audio File ✅

**Steps:**
1. Open application
2. Click on upload area or drag & drop audio file
3. Select a valid MP3/WAV file (< 50MB)
4. Verify file name and size display
5. Click "Summarize Lecture" button

**Expected Results:**
- ✅ File name appears in preview
- ✅ File size displayed correctly
- ✅ "Summarize" button becomes enabled
- ✅ Loading spinner appears
- ✅ Output section displays with 3 tabs
- ✅ Transcript shows full text
- ✅ Summary shows condensed version
- ✅ Key Points shows bullet list
- ✅ Word counts displayed

**Pass Criteria:** All output sections populated correctly

---

### Test 2: Upload Invalid File Format ❌

**Steps:**
1. Click upload area
2. Select a non-audio file (e.g., .txt, .pdf, .jpg)
3. Observe error message

**Expected Results:**
- ✅ Error message: "Unsupported file format"
- ✅ List of supported formats shown
- ✅ File not accepted
- ✅ Summarize button remains disabled

**Pass Criteria:** Clear error message, file rejected

---

### Test 3: Upload File Exceeding Size Limit ❌

**Steps:**
1. Attempt to upload file > 50MB
2. Observe validation

**Expected Results:**
- ✅ Error message: "File size exceeds 50MB limit"
- ✅ File not processed
- ✅ No upload to server

**Pass Criteria:** Size validation working

---

### Test 4: No File Upload Validation ⚠️

**Steps:**
1. Don't upload any file
2. Try to click Summarize button (should be disabled)
3. Or upload, remove file, try to summarize

**Expected Results:**
- ✅ Summarize button disabled initially
- ✅ After file removal, button disabled again
- ✅ If forced, shows: "Please upload or record an audio file first"

**Pass Criteria:** Proper validation prevents empty submission

---

### Test 5: Audio Recording Feature 🎤

**Steps:**
1. Click "Record Audio" tab
2. Click "Start Recording" button
3. Allow microphone permission if prompted
4. Speak for 10-15 seconds
5. Click "Stop Recording"
6. Verify audio preview appears

**Expected Results:**
- ✅ Recording status shows "Recording..."
- ✅ Status indicator blinks red
- ✅ Timer shows duration
- ✅ Live transcript displays (if supported)
- ✅ Audio player appears after stop
- ✅ Can play recorded audio
- ✅ Summarize button enabled

**Pass Criteria:** Recording works end-to-end

---

### Test 6: Live Transcript Display 📝

**Steps:**
1. Go to Record tab
2. Start recording
3. Speak clearly
4. Watch live transcript area

**Expected Results:**
- ✅ Live transcript section appears
- ✅ Text appears as you speak
- ✅ Updates in real-time
- ✅ Shows "Listening..." when active

**Pass Criteria:** Real-time speech recognition working

---

### Test 7: Download Notes Feature 📥

**Steps:**
1. Process an audio file
2. Wait for results
3. Click "Download" button
4. Check downloaded file

**Expected Results:**
- ✅ File downloads automatically
- ✅ Filename: `lecture-notes-[timestamp].txt`
- ✅ File contains:
  - Header with timestamp
  - Full transcript
  - Summary section
  - Key points list
  - Footer

**Pass Criteria:** Complete notes exported correctly

---

### Test 8: Copy to Clipboard Feature 📋

**Steps:**
1. Process audio file
2. Navigate to Summary tab
3. Click "Copy" button
4. Paste in text editor

**Expected Results:**
- ✅ Toast notification: "Copied to clipboard!"
- ✅ Content pastes correctly
- ✅ Works for all tabs (Transcript, Summary, Key Points)

**Pass Criteria:** Clipboard functionality working

---

### Test 9: Dark Mode Toggle 🌙

**Steps:**
1. Click moon/sun icon (top right)
2. Observe theme change
3. Click again to toggle back

**Expected Results:**
- ✅ Theme switches between light/dark
- ✅ Icon changes (moon ↔ sun)
- ✅ All colors update properly
- ✅ Theme persists on refresh
- ✅ Smooth transition animation

**Pass Criteria:** Theme toggle fully functional

---

### Test 10: Search in Notes 🔍

**Steps:**
1. Process audio file with substantial content
2. Type a word in search bar
3. Observe highlighting
4. Clear search

**Expected Results:**
- ✅ Search bar functional
- ✅ Matching text highlighted in yellow
- ✅ Works across all tabs
- ✅ Clear button appears when typing
- ✅ Highlights removed when cleared

**Pass Criteria:** Search and highlight working

---

## 🎨 UI/UX Quality Tests

### Visual Design

- [ ] Clean, modern interface
- [ ] Consistent color scheme
- [ ] Proper spacing and alignment
- [ ] Professional typography
- [ ] Smooth animations
- [ ] No visual glitches

### Responsiveness

- [ ] Works on desktop (1920x1080)
- [ ] Works on laptop (1366x768)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)
- [ ] No horizontal scrolling
- [ ] Touch-friendly buttons

### User Feedback

- [ ] Loading indicator visible
- [ ] Success messages shown
- [ ] Error messages clear
- [ ] Button states (disabled/enabled)
- [ ] Hover effects present
- [ ] Toast notifications work

---

## 🔗 API Integration Tests

### Backend Connection

**Test Endpoint: GET /health**
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "healthy", "model": "whisper-base"}`

**Test Endpoint: POST /summarize**
```bash
curl -X POST http://localhost:5000/summarize \
  -F "audio=@test.mp3"
```
Expected: JSON with transcript, summary, key_points

**Test Endpoint: GET /**
```bash
curl http://localhost:5000/
```
Expected: API information

---

## 📊 Performance Tests

### Speed Benchmarks

| Audio Length | Expected Processing Time |
|--------------|-------------------------|
| 1 minute | ~30-60 seconds |
| 5 minutes | ~3-5 minutes |
| 10 minutes | ~6-10 minutes |

### Resource Usage

- [ ] No memory leaks
- [ ] Files cleaned up after processing
- [ ] Browser doesn't freeze during processing
- [ ] Smooth scrolling in output

---

## 🌐 Browser Compatibility

| Browser | Upload | Recording | Dark Mode | Search |
|---------|--------|-----------|-----------|--------|
| Chrome | ✅ | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ | ✅ |
| Firefox | ✅ | ⚠️ | ✅ | ✅ |
| Safari | ✅ | ⚠️ | ✅ | ✅ |

⚠️ Recording may have limited support in Firefox/Safari

---

## 🚨 Error Handling Tests

### Network Errors

- [ ] Backend not running → Clear error message
- [ ] Slow connection → Loading timeout
- [ ] Server error → Graceful fallback

### File Errors

- [ ] Corrupted audio → Error message
- [ ] Empty file → Validation error
- [ ] Wrong extension → Format error

### Permission Errors

- [ ] Microphone denied → Helpful message
- [ ] Camera access (if needed) → Proper handling

---

## 📱 Mobile Testing

### Touch Interactions

- [ ] Tap to upload works
- [ ] Drag & drop adapted for mobile
- [ ] Buttons are touch-friendly (min 44px)
- [ ] No hover-dependent features
- [ ] Keyboard doesn't break layout

### Mobile Layout

- [ ] Header scales properly
- [ ] Cards stack vertically
- [ ] Tabs remain accessible
- [ ] Text remains readable
- [ ] No overflow issues

---

## ♿ Accessibility Tests

- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Focus indicators visible
- [ ] Alt text on icons (where applicable)
- [ ] Color contrast sufficient
- [ ] Screen reader friendly

---

## 🎯 Demo Flow for Judges (5 Minutes)

### Minute 1: Introduction
1. Show landing page
2. Explain features
3. Highlight clean UI

### Minute 2: Upload Demo
1. Upload sample lecture audio
2. Show file preview
3. Click Summarize
4. Show loading state

### Minute 3: Results Display
1. Show Transcript tab
2. Switch to Summary tab
3. Show Key Points tab
4. Demonstrate search feature

### Minute 4: Advanced Features
1. Toggle dark mode
2. Copy summary to clipboard
3. Download notes
4. Show history panel

### Minute 5: Recording Demo
1. Switch to Record tab
2. Record short sample
3. Show live transcript
4. Process recording
5. Show results

---

## ✅ Final Checklist

### Before Demo
- [ ] Backend running
- [ ] Test files ready
- [ ] Microphone working
- [ ] Internet connection stable
- [ ] Browser console clear
- [ ] Demo script prepared

### During Demo
- [ ] Speak clearly
- [ ] Show all features
- [ ] Explain technical choices
- [ ] Handle errors gracefully
- [ ] Keep within time limit

### After Demo
- [ ] Answer questions
- [ ] Show code structure
- [ ] Explain future enhancements
- [ ] Provide documentation

---

## 📈 Scoring Rubric (For Judges)

| Category | Weight | Score |
|----------|--------|-------|
| Functionality | 30% | /30 |
| UI/UX Design | 25% | /25 |
| Code Quality | 20% | /20 |
| Innovation | 15% | /15 |
| Documentation | 10% | /10 |
| **Total** | **100%** | **/100** |

---

**Testing completed: ___________**

**Tester signature: ___________**

**Date: ___________**
