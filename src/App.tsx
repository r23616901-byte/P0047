import { useState } from 'react';
import AudioUploader from './components/AudioUploader';
import FilePreview from './components/FilePreview';
import TranscriptDisplay from './components/TranscriptDisplay';

// Backend API URL - change this if your backend runs on a different port
const API_URL = 'http://localhost:5000';

export default function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [language, setLanguage] = useState<string>('');
  const [duration, setDuration] = useState<number>(0);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError('');
    setTranscript('');
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setTranscript('');
    setError('');
  };

  const handleConvert = async () => {
    if (!selectedFile) {
      setError('Please select an audio file first');
      return;
    }

    setIsLoading(true);
    setError('');
    setTranscript('');

    try {
      // Create form data for file upload
      const formData = new FormData();
      formData.append('audio', selectedFile);

      // Send request to backend
      const response = await fetch(`${API_URL}/transcribe`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Transcription failed');
      }

      if (!data.success) {
        throw new Error(data.error || 'Transcription failed');
      }

      // Set the transcript and metadata
      setTranscript(data.transcript);
      setLanguage(data.language || '');
      setDuration(data.duration || 0);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      
      // Check if it's a connection error
      if (errorMessage.includes('Failed to fetch') || errorMessage.includes('NetworkError')) {
        setError(
          'Cannot connect to backend server. Please ensure the backend is running on http://localhost:5000'
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyTranscript = async () => {
    if (transcript) {
      try {
        await navigator.clipboard.writeText(transcript);
        alert('Transcript copied to clipboard!');
      } catch {
        alert('Failed to copy transcript');
      }
    }
  };

  const handleDownloadTranscript = () => {
    if (transcript) {
      const blob = new Blob([transcript], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `transcript-${new Date().toISOString().slice(0, 10)}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="flex items-center gap-4">
            {/* Logo */}
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-200">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </svg>
            </div>

            {/* Title */}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                AI-Based Lecture Summarizer
              </h1>
              <p className="text-sm text-gray-500">
                Task 1: Audio to Text Conversion
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <div className="space-y-6">
          {/* Upload Section */}
          <section>
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                />
              </svg>
              Step 1: Upload Audio File
            </h2>
            <AudioUploader
              onFileSelect={handleFileSelect}
              disabled={isLoading}
            />
          </section>

          {/* File Preview & Convert Button */}
          {selectedFile && (
            <section className="space-y-4">
              <FilePreview
                file={selectedFile}
                onRemove={handleRemoveFile}
                disabled={isLoading}
              />

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
                  <svg className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p className="text-red-700">{error}</p>
                </div>
              )}

              {/* Convert Button */}
              <button
                onClick={handleConvert}
                disabled={isLoading}
                className={`
                  w-full py-4 px-6 rounded-xl font-semibold text-white
                  transition-all duration-300 ease-in-out
                  flex items-center justify-center gap-3
                  ${isLoading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-200 hover:shadow-xl hover:shadow-indigo-300'
                  }
                `}
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Converting...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <span>Convert to Text</span>
                  </>
                )}
              </button>
            </section>
          )}

          {/* Transcript Section */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                Step 2: View Transcript
              </h2>
              {transcript && (
                <div className="flex gap-2">
                  <button
                    onClick={handleCopyTranscript}
                    className="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors flex items-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    Copy
                  </button>
                  <button
                    onClick={handleDownloadTranscript}
                    className="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors flex items-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                      />
                    </svg>
                    Download
                  </button>
                </div>
              )}
            </div>
            <TranscriptDisplay
              transcript={transcript}
              isLoading={isLoading}
              language={language}
              duration={duration}
            />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 border-t border-gray-200 bg-white">
        <div className="max-w-5xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>AI-Based Lecture Summarizer &copy; 2026</p>
          <p className="mt-1">Powered by OpenAI Whisper</p>
        </div>
      </footer>
    </div>
  );
}
