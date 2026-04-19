/**
 * AI Lecture Summarizer - Frontend JavaScript
 * Complete functionality for audio upload, recording, transcription, and summarization
 */

// ============================================
// Global Variables
// ============================================
let selectedFile = null;
let recordedAudioBlob = null;
let mediaRecorder = null;
let audioChunks = [];
let speechRecognition = null;
let isRecording = false;
let recordingStartTime = null;
let recordingTimer = null;

// API Configuration
const API_BASE_URL = 'http://localhost:5000'; // Backend Flask server

// ============================================
// DOM Elements
// ============================================
const elements = {
    // Dark Mode
    darkModeToggle: document.getElementById('darkModeToggle'),
    
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    uploadTab: document.getElementById('uploadTab'),
    recordTab: document.getElementById('recordTab'),
    
    // Upload
    uploadArea: document.getElementById('uploadArea'),
    audioFile: document.getElementById('audioFile'),
    filePreview: document.getElementById('filePreview'),
    fileName: document.getElementById('fileName'),
    fileSize: document.getElementById('fileSize'),
    removeFileBtn: document.getElementById('removeFileBtn'),
    
    // Recording
    startRecordBtn: document.getElementById('startRecordBtn'),
    stopRecordBtn: document.getElementById('stopRecordBtn'),
    recordingStatus: document.getElementById('recordingStatus'),
    liveTranscript: document.getElementById('liveTranscript'),
    liveTranscriptText: document.getElementById('liveTranscriptText'),
    audioPreview: document.getElementById('audioPreview'),
    recordedAudio: document.getElementById('recordedAudio'),
    recordingDuration: document.getElementById('recordingDuration'),
    reRecordBtn: document.getElementById('reRecordBtn'),
    
    // Actions
    summarizeBtn: document.getElementById('summarizeBtn'),
    loadingContainer: document.getElementById('loadingContainer'),
    errorMessage: document.getElementById('errorMessage'),
    errorText: document.getElementById('errorText'),
    successMessage: document.getElementById('successMessage'),
    
    // Output
    outputSection: document.getElementById('outputSection'),
    outputTabs: document.querySelectorAll('.output-tab'),
    transcriptContent: document.getElementById('transcriptContent'),
    summaryContent: document.getElementById('summaryContent'),
    keypointsContent: document.getElementById('keypointsContent'),
    transcriptText: document.getElementById('transcriptText'),
    summaryText: document.getElementById('summaryText'),
    keypointsList: document.getElementById('keypointsList'),
    transcriptWordCount: document.getElementById('transcriptWordCount'),
    summaryWordCount: document.getElementById('summaryWordCount'),
    pointsCount: document.getElementById('pointsCount'),
    
    // Actions
    copyBtn: document.getElementById('copyBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    newSessionBtn: document.getElementById('newSessionBtn'),
    
    // Search
    searchInput: document.getElementById('searchInput'),
    clearSearch: document.getElementById('clearSearch'),
    
    // History
    historySection: document.getElementById('historySection'),
    historyList: document.getElementById('historyList'),
    showHistoryLink: document.getElementById('showHistoryLink'),
    
    // Toast
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toastMessage')
};

// ============================================
// Initialize Application
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initializeDarkMode();
    initializeTabs();
    initializeUpload();
    initializeRecording();
    initializeOutputTabs();
    initializeActions();
    initializeSearch();
    loadHistory();
    
    console.log('✅ AI Lecture Summarizer initialized');
});

// ============================================
// Dark Mode Functionality
// ============================================
function initializeDarkMode() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateDarkModeIcon(savedTheme);
    
    elements.darkModeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateDarkModeIcon(newTheme);
        showToast(`Switched to ${newTheme} mode`);
    });
}

function updateDarkModeIcon(theme) {
    const icon = elements.darkModeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// ============================================
// Tab Navigation (Upload/Record)
// ============================================
function initializeTabs() {
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            // Update button states
            elements.tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content visibility
            elements.uploadTab.classList.remove('active');
            elements.recordTab.classList.remove('active');
            
            if (tab === 'upload') {
                elements.uploadTab.classList.add('active');
            } else {
                elements.recordTab.classList.add('active');
            }
            
            // Reset states
            resetUploadState();
        });
    });
}

// ============================================
// File Upload Functionality
// ============================================
function initializeUpload() {
    // Click to upload
    elements.uploadArea.addEventListener('click', () => {
        elements.audioFile.click();
    });
    
    // File input change
    elements.audioFile.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFileSelect(file);
    });
    
    // Drag and drop
    elements.uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.add('dragover');
    });
    
    elements.uploadArea.addEventListener('dragleave', () => {
        elements.uploadArea.classList.remove('dragover');
    });
    
    elements.uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        handleFileSelect(file);
    });
    
    // Remove file
    elements.removeFileBtn.addEventListener('click', () => {
        resetUploadState();
    });
}

function handleFileSelect(file) {
    if (!file) return;
    
    // Validate file type
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/ogg', 'audio/flac'];
    const validExtensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        showError('Unsupported file format. Please upload MP3, WAV, M4A, OGG, or FLAC.');
        return;
    }
    
    // Validate file size (50MB limit)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File size exceeds 50MB limit. Please upload a smaller file.');
        return;
    }
    
    // Set file
    selectedFile = file;
    recordedAudioBlob = null; // Clear any recorded audio
    
    // Update UI
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatFileSize(file.size);
    elements.filePreview.classList.remove('hidden');
    elements.uploadArea.classList.add('hidden');
    
    // Enable summarize button
    elements.summarizeBtn.disabled = false;
    
    // Hide any previous errors
    hideError();
    
    console.log('✅ File selected:', file.name);
}

function resetUploadState() {
    selectedFile = null;
    elements.audioFile.value = '';
    elements.filePreview.classList.add('hidden');
    elements.uploadArea.classList.remove('hidden');
    elements.summarizeBtn.disabled = true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// ============================================
// Audio Recording Functionality (Web Speech API)
// ============================================
function initializeRecording() {
    // Check browser support for MediaRecorder
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        elements.startRecordBtn.disabled = true;
        elements.startRecordBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Recording Not Supported</span>';
        console.warn('MediaRecorder API not supported');
    }
    
    // Initialize Speech Recognition
    initializeSpeechRecognition();
    
    // Start Recording
    elements.startRecordBtn.addEventListener('click', startRecording);
    
    // Stop Recording
    elements.stopRecordBtn.addEventListener('click', stopRecording);
    
    // Re-record
    elements.reRecordBtn.addEventListener('click', () => {
        elements.audioPreview.classList.add('hidden');
        elements.startRecordBtn.classList.remove('hidden');
        elements.stopRecordBtn.classList.add('hidden');
        recordedAudioBlob = null;
        elements.summarizeBtn.disabled = true;
    });
}

function initializeSpeechRecognition() {
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = true;
        speechRecognition.interimResults = true;
        speechRecognition.lang = 'en-US';
        
        speechRecognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            elements.liveTranscriptText.textContent = finalTranscript + interimTranscript || 'Listening...';
        };
        
        speechRecognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error === 'not-allowed') {
                showError('Microphone access denied. Please allow microphone permissions.');
            }
        };
        
        console.log('✅ Speech Recognition initialized');
    } else {
        console.warn('Speech Recognition API not supported in this browser');
        elements.liveTranscript.classList.add('hidden');
    }
}

async function startRecording() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Start MediaRecorder
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            recordedAudioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(recordedAudioBlob);
            elements.recordedAudio.src = audioUrl;
            elements.audioPreview.classList.remove('hidden');
            elements.summarizeBtn.disabled = false;
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
        };
        
        // Start recording
        mediaRecorder.start();
        isRecording = true;
        recordingStartTime = Date.now();
        
        // Start speech recognition if available
        if (speechRecognition) {
            speechRecognition.start();
            elements.liveTranscript.classList.remove('hidden');
        }
        
        // Update UI
        elements.startRecordBtn.classList.add('hidden');
        elements.stopRecordBtn.classList.remove('hidden');
        elements.recordingStatus.querySelector('.status-indicator').classList.add('recording');
        elements.recordingStatus.querySelector('span').textContent = 'Recording...';
        
        // Start timer
        startRecordingTimer();
        
        console.log('🎤 Recording started');
        
    } catch (error) {
        console.error('Error starting recording:', error);
        if (error.name === 'NotAllowedError') {
            showError('Microphone access denied. Please allow microphone permissions in your browser.');
        } else {
            showError('Failed to start recording. Please check your microphone.');
        }
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // Stop speech recognition
        if (speechRecognition) {
            speechRecognition.stop();
        }
        
        // Stop timer
        stopRecordingTimer();
        
        // Update UI
        elements.startRecordBtn.classList.remove('hidden');
        elements.stopRecordBtn.classList.add('hidden');
        elements.recordingStatus.querySelector('.status-indicator').classList.remove('recording');
        elements.recordingStatus.querySelector('span').textContent = 'Recording Complete';
        
        console.log('⏹️ Recording stopped');
    }
}

function startRecordingTimer() {
    const updateTimer = () => {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        elements.recordingDuration.textContent = `${minutes}:${seconds}`;
    };
    
    updateTimer();
    recordingTimer = setInterval(updateTimer, 1000);
}

function stopRecordingTimer() {
    if (recordingTimer) {
        clearInterval(recordingTimer);
        recordingTimer = null;
    }
}

// ============================================
// Output Tabs (Transcript/Summary/Key Points)
// ============================================
function initializeOutputTabs() {
    elements.outputTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const output = tab.dataset.output;
            
            // Update button states
            elements.outputTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update content visibility
            elements.transcriptContent.classList.remove('active');
            elements.summaryContent.classList.remove('active');
            elements.keypointsContent.classList.remove('active');
            
            if (output === 'transcript') {
                elements.transcriptContent.classList.add('active');
            } else if (output === 'summary') {
                elements.summaryContent.classList.add('active');
            } else {
                elements.keypointsContent.classList.add('active');
            }
        });
    });
}

// ============================================
// Summarize Action (API Integration)
// ============================================
function initializeActions() {
    elements.summarizeBtn.addEventListener('click', handleSummarize);
    elements.copyBtn.addEventListener('click', handleCopy);
    elements.downloadBtn.addEventListener('click', handleDownload);
    elements.newSessionBtn.addEventListener('click', handleNewSession);
    elements.showHistoryLink.addEventListener('click', (e) => {
        e.preventDefault();
        elements.historySection.classList.toggle('hidden');
    });
}

async function handleSummarize() {
    // Validate input
    if (!selectedFile && !recordedAudioBlob) {
        showError('Please upload or record an audio file first.');
        return;
    }
    
    // Show loading state
    showLoading(true);
    hideError();
    elements.outputSection.classList.add('hidden');
    
    try {
        // Prepare form data
        const formData = new FormData();
        
        if (selectedFile) {
            formData.append('audio', selectedFile);
        } else if (recordedAudioBlob) {
            formData.append('audio', recordedAudioBlob, 'recording.wav');
        }
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process audio');
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
        // Save to history
        saveToHistory(data);
        
        // Show success message
        elements.successMessage.classList.remove('hidden');
        setTimeout(() => {
            elements.successMessage.classList.add('hidden');
        }, 3000);
        
        console.log('✅ Summarization complete');
        
    } catch (error) {
        console.error('Summarization error:', error);
        
        // Fallback: Display mock data for demonstration
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            showError('Backend server not available. Running in demo mode with sample data.');
            displayDemoResults();
        } else {
            showError(error.message || 'An error occurred while processing. Please try again.');
        }
    } finally {
        showLoading(false);
    }
}

function displayResults(data) {
    // Transcript
    elements.transcriptText.textContent = data.transcript || 'No transcript available';
    elements.transcriptWordCount.textContent = `${countWords(data.transcript)} words`;
    
    // Summary
    elements.summaryText.textContent = data.summary || 'No summary available';
    elements.summaryWordCount.textContent = `${countWords(data.summary)} words`;
    
    // Key Points
    const keyPoints = data.key_points || data.keyPoints || [];
    elements.keypointsList.innerHTML = '';
    if (keyPoints.length > 0) {
        keyPoints.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point;
            elements.keypointsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No key points extracted';
        elements.keypointsList.appendChild(li);
    }
    elements.pointsCount.textContent = `${keyPoints.length} points`;
    
    // Show output section
    elements.outputSection.classList.remove('hidden');
    
    // Scroll to output
    elements.outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayDemoResults() {
    // Demo data for when backend is not available
    const demoData = {
        transcript: `Welcome to today's lecture on Machine Learning fundamentals. 

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. Today we'll cover three main types of machine learning.

First, supervised learning, where the model is trained on labeled data. Examples include classification tasks like spam detection and regression tasks like price prediction.

Second, unsupervised learning, where the model finds patterns in unlabeled data. Common techniques include clustering for customer segmentation and dimensionality reduction for data visualization.

Third, reinforcement learning, where an agent learns to make decisions by interacting with an environment and receiving rewards or penalties.

Key algorithms we discussed include linear regression, logistic regression, decision trees, random forests, support vector machines, and neural networks.

Remember, the choice of algorithm depends on your data type, problem type, and performance requirements. Always start with simple models before moving to complex ones.

For next class, please review the concepts of overfitting and underfitting, and complete the practice exercises on the learning portal.`,
        
        summary: `This lecture covered the fundamentals of Machine Learning, including its three main types: supervised learning (trained on labeled data for tasks like classification and regression), unsupervised learning (finding patterns in unlabeled data through clustering and dimensionality reduction), and reinforcement learning (agents learning through environmental interaction). Key algorithms discussed include linear regression, decision trees, random forests, SVMs, and neural networks. The importance of starting with simple models and understanding overfitting/underfitting was emphasized.`,
        
        key_points: [
            'Machine Learning is a subset of AI that learns from experience without explicit programming',
            'Supervised Learning uses labeled data for classification and regression tasks',
            'Unsupervised Learning finds patterns in unlabeled data through clustering',
            'Reinforcement Learning involves agents learning through rewards and penalties',
            'Key algorithms: Linear Regression, Decision Trees, Random Forests, SVMs, Neural Networks',
            'Start with simple models before moving to complex ones',
            'Understanding overfitting and underfitting is crucial for model performance'
        ]
    };
    
    displayResults(demoData);
}

function countWords(text) {
    if (!text) return 0;
    return text.trim().split(/\s+/).length;
}

function showLoading(show) {
    if (show) {
        elements.loadingContainer.classList.remove('hidden');
        elements.summarizeBtn.disabled = true;
    } else {
        elements.loadingContainer.classList.add('hidden');
        elements.summarizeBtn.disabled = false;
    }
}

function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.classList.remove('hidden');
}

function hideError() {
    elements.errorMessage.classList.add('hidden');
}

// ============================================
// Copy Functionality
// ============================================
function handleCopy() {
    const activeTab = document.querySelector('.output-tab.active').dataset.output;
    let textToCopy = '';
    
    if (activeTab === 'transcript') {
        textToCopy = elements.transcriptText.textContent;
    } else if (activeTab === 'summary') {
        textToCopy = elements.summaryText.textContent;
    } else {
        textToCopy = Array.from(elements.keypointsList.querySelectorAll('li'))
            .map(li => `• ${li.textContent}`).join('\n');
    }
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        showToast('Copied to clipboard!');
    }).catch(err => {
        console.error('Copy failed:', err);
        showError('Failed to copy. Please select and copy manually.');
    });
}

// ============================================
// Download Functionality
// ============================================
function handleDownload() {
    const transcript = elements.transcriptText.textContent;
    const summary = elements.summaryText.textContent;
    const keyPoints = Array.from(elements.keypointsList.querySelectorAll('li'))
        .map(li => `• ${li.textContent}`).join('\n');
    
    const content = `AI LECTURE SUMMARIZER
=====================
Generated: ${new Date().toLocaleString()}

---------------------------------
TRANSCRIPT
---------------------------------
${transcript}

---------------------------------
SUMMARY
---------------------------------
${summary}

---------------------------------
KEY POINTS
---------------------------------
${keyPoints}

=====================
Powered by AI Lecture Summarizer
`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lecture-notes-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('Notes downloaded successfully!');
}

// ============================================
// New Session
// ============================================
function handleNewSession() {
    // Reset upload
    resetUploadState();
    
    // Reset recording
    if (elements.audioPreview) {
        elements.audioPreview.classList.add('hidden');
    }
    recordedAudioBlob = null;
    
    // Hide output
    elements.outputSection.classList.add('hidden');
    
    // Reset search
    elements.searchInput.value = '';
    elements.clearSearch.classList.add('hidden');
    
    // Reset tabs
    elements.tabBtns[0].click();
    elements.outputTabs[0].click();
    
    showToast('New session started');
}

// ============================================
// Search Functionality
// ============================================
function initializeSearch() {
    elements.searchInput.addEventListener('input', handleSearch);
    elements.clearSearch.addEventListener('click', clearSearch);
}

function handleSearch() {
    const query = elements.searchInput.value.toLowerCase().trim();
    
    if (query.length > 0) {
        elements.clearSearch.classList.remove('hidden');
        highlightText(query);
    } else {
        elements.clearSearch.classList.add('hidden');
        removeHighlights();
    }
}

function clearSearch() {
    elements.searchInput.value = '';
    elements.clearSearch.classList.add('hidden');
    removeHighlights();
}

function highlightText(query) {
    removeHighlights();
    
    const activeContent = document.querySelector('.output-tab-content.active');
    if (!activeContent) return;
    
    const textElements = activeContent.querySelectorAll('p, li');
    
    textElements.forEach(el => {
        const originalText = el.textContent;
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        el.innerHTML = originalText.replace(regex, '<span class="highlight">$1</span>');
    });
}

function removeHighlights() {
    const highlightedElements = document.querySelectorAll('.highlight');
    highlightedElements.forEach(el => {
        const parent = el.parentNode;
        parent.replaceChild(document.createTextNode(el.textContent), el);
        parent.normalize();
    });
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ============================================
// History Management
// ============================================
function saveToHistory(data) {
    const history = getHistory();
    const historyItem = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        summary: data.summary?.substring(0, 100) + '...' || 'No summary',
        transcript: data.transcript,
        summary_full: data.summary,
        key_points: data.key_points || data.keyPoints || []
    };
    
    history.unshift(historyItem);
    
    // Keep only last 10 items
    if (history.length > 10) {
        history.pop();
    }
    
    localStorage.setItem('lectureHistory', JSON.stringify(history));
    loadHistory();
}

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem('lectureHistory')) || [];
    } catch {
        return [];
    }
}

function loadHistory() {
    const history = getHistory();
    
    if (history.length === 0) {
        elements.historyList.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 20px;">No history yet</p>';
        return;
    }
    
    elements.historyList.innerHTML = '';
    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div class="history-item-info">
                <h4>${item.timestamp}</h4>
                <span>${item.summary}</span>
            </div>
            <i class="fas fa-chevron-right"></i>
        `;
        
        historyItem.addEventListener('click', () => {
            loadHistoryItem(item);
            elements.historySection.classList.add('hidden');
        });
        
        elements.historyList.appendChild(historyItem);
    });
}

function loadHistoryItem(item) {
    displayResults({
        transcript: item.transcript,
        summary: item.summary_full,
        key_points: item.key_points
    });
    showToast('History item loaded');
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message) {
    elements.toastMessage.textContent = message;
    elements.toast.classList.add('show');
    
    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

// ============================================
// Utility Functions
// ============================================
function isBrowserSupported() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

// Log browser support on load
console.log('🎤 MediaRecorder supported:', isBrowserSupported());
console.log('🗣️ Speech Recognition supported:', !!(window.SpeechRecognition || window.webkitSpeechRecognition));
