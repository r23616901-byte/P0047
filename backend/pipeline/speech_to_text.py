"""
Speech-to-Text Module
Uses OpenAI Whisper for audio transcription
"""

import os
import tempfile
from typing import Dict, Optional
from pathlib import Path


class SpeechToText:
    """
    Convert speech audio to text using Whisper model
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Speech-to-Text with Whisper model
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self._model_loaded = False
        
    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self._model_loaded:
            return
        
        try:
            import whisper
            print(f"Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            self._model_loaded = True
            print(f"Whisper model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str, language: str = None) -> Dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., 'en', 'es')
            
        Returns:
            Dictionary with transcript and metadata
        """
        if not self._model_loaded:
            self.load_model()
        
        if not os.path.exists(audio_path):
            return {
                'success': False,
                'error': f'Audio file not found: {audio_path}',
                'transcript': '',
                'language': None,
                'duration': 0
            }
        
        try:
            # Transcribe audio
            options = {}
            if language:
                options['language'] = language
            
            result = self.model.transcribe(audio_path, **options)
            
            transcript = result.get('text', '').strip()
            language = result.get('language', 'unknown')
            
            # Get duration from segments
            duration = 0
            if result.get('segments'):
                duration = result['segments'][-1].get('end', 0)
            
            return {
                'success': True,
                'transcript': transcript,
                'language': language,
                'duration': duration,
                'segments': result.get('segments', [])
            }
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return {
                'success': False,
                'error': str(e),
                'transcript': '',
                'language': None,
                'duration': 0
            }
    
    def transcribe_bytes(self, audio_bytes: bytes, file_extension: str = '.wav') -> Dict:
        """
        Transcribe audio from bytes
        
        Args:
            audio_bytes: Raw audio bytes
            file_extension: File extension for temporary file
            
        Returns:
            Dictionary with transcript and metadata
        """
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        )
        temp_path = temp_file.name
        
        try:
            # Write bytes to temp file
            temp_file.write(audio_bytes)
            temp_file.close()
            
            # Transcribe
            result = self.transcribe(temp_path)
            
            return result
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def get_supported_formats(self) -> list:
        """Get list of supported audio formats"""
        return ['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm', 'mov', 'mp4']
    
    def validate_audio_file(self, file_path: str) -> tuple:
        """
        Validate audio file
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        ext = Path(file_path).suffix.lower().lstrip('.')
        if ext not in self.get_supported_formats():
            return False, f"Unsupported format: {ext}"
        
        # Check file size (max 50MB)
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:
            return False, "File too large (max 50MB)"
        
        return True, None
