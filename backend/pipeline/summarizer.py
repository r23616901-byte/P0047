"""
Summarizer Module
Uses BART Transformer model for abstractive summarization
"""

import re
from typing import Dict, Optional


class Summarizer:
    """
    Generate summaries using BART transformer model
    """
    
    def __init__(self, model_name: str = "facebook/bart-base"):
        """
        Initialize the summarizer with BART model
        
        Args:
            model_name: HuggingFace model name (facebook/bart-base, facebook/bart-large-cnn)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self._model_loaded = False
        
    def load_model(self):
        """
        Load BART model and tokenizer (lazy loading)
        """
        if self._model_loaded:
            return
        
        try:
            from transformers import BartTokenizer, BartForConditionalGeneration
            import torch
            
            print(f"Loading BART model: {self.model_name}...")
            
            self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
            self.model = BartForConditionalGeneration.from_pretrained(self.model_name)
            
            # Set device
            if torch.cuda.is_available():
                self.device = "cuda"
                self.model = self.model.to(self.device)
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = "mps"
                self.model = self.model.to(self.device)
            
            self.model.eval()
            self._model_loaded = True
            print(f"BART model loaded successfully on {self.device}!")
            
        except Exception as e:
            print(f"Error loading BART model: {e}")
            print("Falling back to extractive summarization...")
            self._model_loaded = False
    
    def _prepare_text(self, text: str, max_length: int = 1024) -> str:
        """
        Prepare text for BART model
        
        Args:
            text: Input text
            max_length: Maximum input length
            
        Returns:
            Formatted text for BART
        """
        text = text.strip()
        
        # Truncate if too long
        words = text.split()
        if len(words) > max_length:
            text = ' '.join(words[:max_length])
        
        return text
    
    def _extractive_summary(self, text: str, max_length: int = 150) -> str:
        """
        Fallback extractive summarization
        
        Args:
            text: Input text
            max_length: Maximum summary length
            
        Returns:
            Extractive summary
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        if len(sentences) <= 2:
            return text
        
        # Take first, middle, and last sentences
        summary_sentences = [sentences[0]]
        
        if len(sentences) > 3:
            mid = len(sentences) // 2
            summary_sentences.append(sentences[mid])
            if len(sentences) > 5:
                summary_sentences.append(sentences[min(mid + 1, len(sentences) - 2)])
        
        summary_sentences.append(sentences[-1])
        
        summary = '. '.join(summary_sentences) + '.'
        
        # Truncate to max length
        words = summary.split()
        if len(words) > max_length // 5:  # Approximate word to character ratio
            summary = ' '.join(words[:max_length // 5]) + '.'
        
        return summary
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 40) -> Dict:
        """
        Generate summary from text
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Dictionary with summary and metadata
        """
        if not text or len(text.strip()) < 50:
            return {
                'summary': text,
                'method': 'passthrough',
                'original_length': len(text),
                'summary_length': len(text)
            }
        
        # Load model if not loaded
        if not self._model_loaded:
            self.load_model()
        
        # If model failed to load, use extractive summary
        if not self._model_loaded:
            summary = self._extractive_summary(text, max_length)
            return {
                'summary': summary,
                'method': 'extractive',
                'original_length': len(text),
                'summary_length': len(summary)
            }
        
        try:
            # Prepare input
            input_text = self._prepare_text(text)
            
            # Tokenize
            inputs = self.tokenizer(
                input_text,
                max_length=1024,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate summary
            summary_ids = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            
            # Decode summary
            summary = self.tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )
            
            return {
                'summary': summary,
                'method': 'bart',
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': round(len(text) / max(len(summary), 1), 2)
            }
            
        except Exception as e:
            print(f"Summarization error: {e}")
            # Fallback to extractive
            summary = self._extractive_summary(text, max_length)
            return {
                'summary': summary,
                'method': 'extractive_fallback',
                'original_length': len(text),
                'summary_length': len(summary),
                'error': str(e)
            }
