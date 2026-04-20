"""
Main Pipeline Module
Integrates all components: Speech-to-Text → Cleaning → Summarization → Key Points
"""

import os
import tempfile
import time
from typing import Dict, Optional
from pathlib import Path

from .speech_to_text import SpeechToText
from .cleaner import TextCleaner
from .summarizer import Summarizer
from .keypoints import KeyPointsExtractor


class AudioPipeline:
    """
    Complete audio processing pipeline
    """
    
    def __init__(
        self,
        whisper_model: str = "base",
        summarizer_model: str = "facebook/bart-base",
        num_key_points: int = 5
    ):
        """
        Initialize the complete pipeline
        
        Args:
            whisper_model: Whisper model size
            summarizer_model: BART model name
            num_key_points: Number of key points to extract
        """
        self.speech_to_text = SpeechToText(model_name=whisper_model)
        self.cleaner = TextCleaner()
        self.summarizer = Summarizer(model_name=summarizer_model)
        self.keypoints_extractor = KeyPointsExtractor(num_points=num_key_points)
        
        self._initialized = False
    
    def process_audio(self, audio_path: str, language: str = None) -> Dict:
        """
        Process audio file through complete pipeline
        
        Args:
            audio_path: Path to audio file
            language: Optional language code
            
        Returns:
            Dictionary with all outputs
        """
        start_time = time.time()
        
        # Validate audio file
        is_valid, error = self.speech_to_text.validate_audio_file(audio_path)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'processing_time': 0
            }
        
        try:
            # Step 1: Speech-to-Text
            print("Step 1/4: Converting speech to text...")
            stt_result = self.speech_to_text.transcribe(audio_path, language)
            
            if not stt_result['success']:
                return {
                    'success': False,
                    'error': stt_result.get('error', 'Transcription failed'),
                    'processing_time': time.time() - start_time
                }
            
            transcript = stt_result['transcript']
            
            if not transcript:
                return {
                    'success': False,
                    'error': 'No speech detected in audio',
                    'processing_time': time.time() - start_time
                }
            
            # Step 2: Text Cleaning
            print("Step 2/4: Cleaning transcript...")
            clean_result = self.cleaner.clean(transcript)
            cleaned_text = clean_result['cleaned_text']
            
            # Step 3: Summarization
            print("Step 3/4: Generating summary...")
            summary_result = self.summarizer.summarize(cleaned_text)
            summary = summary_result['summary']
            
            # Step 4: Key Points Extraction
            print("Step 4/4: Extracting key points...")
            keypoints_result = self.keypoints_extractor.extract(cleaned_text)
            key_points = keypoints_result['key_points']
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            print(f"✅ Pipeline complete in {processing_time:.2f}s")
            
            return {
                'success': True,
                'transcript': transcript,
                'cleaned_text': cleaned_text,
                'summary': summary,
                'key_points': key_points,
                'language': stt_result.get('language', 'unknown'),
                'duration': stt_result.get('duration', 0),
                'stats': {
                    'transcript_length': len(transcript),
                    'cleaned_length': len(cleaned_text),
                    'summary_length': len(summary),
                    'key_points_count': len(key_points),
                    'fillers_removed': clean_result['stats'].get('fillers_removed', 0),
                    'noise_removed': clean_result['stats'].get('noise_removed', 0),
                    'summarization_method': summary_result.get('method', 'unknown'),
                    'extraction_method': keypoints_result.get('method', 'unknown')
                },
                'processing_time': round(processing_time, 2)
            }
            
        except Exception as e:
            print(f"Pipeline error: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def process_text(self, text: str) -> Dict:
        """
        Process raw text through NLP pipeline (skip speech-to-text)
        
        Args:
            text: Raw transcript text
            
        Returns:
            Dictionary with all outputs
        """
        start_time = time.time()
        
        try:
            # Step 1: Text Cleaning
            print("Step 1/3: Cleaning text...")
            clean_result = self.cleaner.clean(text)
            cleaned_text = clean_result['cleaned_text']
            
            # Step 2: Summarization
            print("Step 2/3: Generating summary...")
            summary_result = self.summarizer.summarize(cleaned_text)
            summary = summary_result['summary']
            
            # Step 3: Key Points Extraction
            print("Step 3/3: Extracting key points...")
            keypoints_result = self.keypoints_extractor.extract(cleaned_text)
            key_points = keypoints_result['key_points']
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            print(f"✅ Text pipeline complete in {processing_time:.2f}s")
            
            return {
                'success': True,
                'cleaned_text': cleaned_text,
                'summary': summary,
                'key_points': key_points,
                'stats': {
                    'original_length': len(text),
                    'cleaned_length': len(cleaned_text),
                    'summary_length': len(summary),
                    'key_points_count': len(key_points),
                    'fillers_removed': clean_result['stats'].get('fillers_removed', 0),
                    'noise_removed': clean_result['stats'].get('noise_removed', 0),
                    'summarization_method': summary_result.get('method', 'unknown'),
                    'extraction_method': keypoints_result.get('method', 'unknown')
                },
                'processing_time': round(processing_time, 2)
            }
            
        except Exception as e:
            print(f"Text pipeline error: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }


def process_audio(audio_path: str, **kwargs) -> Dict:
    """
    Convenience function to process audio file
    
    Args:
        audio_path: Path to audio file
        **kwargs: Additional arguments for AudioPipeline
        
    Returns:
        Dictionary with all outputs
    """
    pipeline = AudioPipeline(**kwargs)
    return pipeline.process_audio(audio_path)


def process_text(text: str, **kwargs) -> Dict:
    """
    Convenience function to process raw text
    
    Args:
        text: Raw transcript text
        **kwargs: Additional arguments for AudioPipeline
        
    Returns:
        Dictionary with all outputs
    """
    pipeline = AudioPipeline(**kwargs)
    return pipeline.process_text(text)
