interface FilePreviewProps {
  file: File | null;
  onRemove: () => void;
  disabled: boolean;
}

export default function FilePreview({ file, onRemove, disabled }: FilePreviewProps) {
  if (!file) return null;

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Get file icon based on extension
  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    const iconColors: Record<string, string> = {
      mp3: 'text-orange-500',
      wav: 'text-blue-500',
      m4a: 'text-purple-500',
      ogg: 'text-green-500',
      flac: 'text-red-500',
    };
    return iconColors[ext || 'mp3'] || 'text-gray-500';
  };

  return (
    <div className="bg-indigo-50 rounded-xl p-4 border border-indigo-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* File Icon */}
          <div className={`w-12 h-12 rounded-lg bg-white flex items-center justify-center shadow-sm ${getFileIcon(file.name)}`}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
              />
            </svg>
          </div>

          {/* File Info */}
          <div>
            <p className="font-medium text-gray-800 truncate max-w-xs">
              {file.name}
            </p>
            <p className="text-sm text-gray-500">
              {formatFileSize(file.size)}
            </p>
          </div>
        </div>

        {/* Remove Button */}
        {!disabled && (
          <button
            onClick={onRemove}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            title="Remove file"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
