import React, { useState, useRef } from 'react';

interface AudioUploaderProps {
  onFileSelect: (file: File) => void;
  disabled: boolean;
}

export default function AudioUploader({ onFileSelect, disabled }: AudioUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedExtensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac'];
  const maxSize = 50 * 1024 * 1024; // 50MB

  const validateFile = (file: File): string | null => {
    // Check file extension
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!allowedExtensions.includes(extension)) {
      return `Unsupported file format. Allowed: ${allowedExtensions.join(', ')}`;
    }

    // Check file size
    if (file.size > maxSize) {
      return 'File too large. Maximum size is 50MB';
    }

    return null;
  };

  const handleFile = (file: File) => {
    const error = validateFile(file);
    if (error) {
      alert(error);
      return;
    }
    onFileSelect(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleClick = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  return (
    <div
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
        transition-all duration-300 ease-in-out
        ${disabled 
          ? 'border-gray-300 bg-gray-50 cursor-not-allowed' 
          : isDragging 
            ? 'border-indigo-500 bg-indigo-50 scale-[1.02]' 
            : 'border-gray-300 hover:border-indigo-400 hover:bg-indigo-50/50'
        }
      `}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".mp3,.wav,.m4a,.ogg,.flac,audio/*"
        onChange={handleInputChange}
        className="hidden"
        disabled={disabled}
      />
      
      <div className="flex flex-col items-center gap-4">
        {/* Upload Icon */}
        <div className={`
          w-16 h-16 rounded-full flex items-center justify-center
          transition-colors duration-300
          ${disabled ? 'bg-gray-200' : 'bg-indigo-100'}
        `}>
          <svg
            className={`w-8 h-8 ${disabled ? 'text-gray-400' : 'text-indigo-600'}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m0-0v-9"
            />
          </svg>
        </div>

        {/* Text Content */}
        <div className="space-y-1">
          <p className={`text-lg font-medium ${disabled ? 'text-gray-400' : 'text-gray-700'}`}>
            {disabled ? 'Processing...' : 'Click or drag audio file here'}
          </p>
          <p className="text-sm text-gray-500">
            Supported: MP3, WAV, M4A, OGG, FLAC (Max 50MB)
          </p>
        </div>
      </div>
    </div>
  );
}
