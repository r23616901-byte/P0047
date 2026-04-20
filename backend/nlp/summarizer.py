"""
Summarizer Module
Uses T5 Transformer model for abstractive summarization
"""

import re
from typing import Dict, Optional


class Summarizer:
    """
    Generate summaries using T5 transformer model
    """
    
    def __init__(self, model_name: str = "t5-small"):
        """
        Initialize the summarizer with T5 model
        
        Args:
            model_name: HuggingFace model name (t5-small, t5-base, etc.)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self._model_loaded = False
        
    def load_model(self):
        """
        Load T5 model and tokenizer (lazy loading)
        """
        if self._model_loaded:
            return
        
        try:
            from transformers import T5Tokenizer, T5ForConditionalGeneration
            import torch
            
            print(f"Loading T5 model: {self.model_name}...")
            
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            
            # Set device
            if torch.cuda.is_available():
                self.device = "cuda"
                self.model = self.model.to(self.device)
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = "mps"
                self.model = self.model.to(self.device)
            
            self.model.eval()
            self._model_loaded = True
            print(f"T5 model loaded successfully on {self.device}!")
            
        except Exception as e:
            print(f"Error loading T5 model: {e}")
            print("Falling back to extractive summarization...")
            self._model_loaded = False
    
    def _prepare_text(self, text: str, max_length: int = 512) -> str:
        """
        Prepare text for T5 model
        
        Args:
            text: Input text
            max_length: Maximum input length
            
        Returns:
            Formatted text for T5
        """
        # T5 expects "summarize: " prefix
        text = text.strip()
        
        # Truncate if too long
        words = text.split()
        if len(words) > max_length:
            text = ' '.join(words[:max_length])
        
        return f"summarize: {text}"
    
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
        
        # Try to load model if not loaded
        if not self._model_loaded:
            self.load_model()
        
        # If model failed to load, use extractive summarization
        if not self._model_loaded:
            return self._extractive_summary(text, max_length)
        
        try:
            import torch
            
            # Prepare input
            input_text = self._prepare_text(text)
            
            # Tokenize
            inputs = self.tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            if self.device != "cpu":
                inputs = inputs.to(self.device)
            
            # Generate summary
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up summary
            summary = self._clean_summary(summary)
            
            return {
                'summary': summary,
                'method': 't5_transformer',
                'model': self.model_name,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': round(len(summary) / len(text) * 100, 2)
            }
            
        except Exception as e:
            print(f"Error during summarization: {e}")
            # Fallback to extractive
            return self._extractive_summary(text, max_length)
    
    def _extractive_summary(self, text: str, max_length: int = 150) -> Dict:
        """
        Fallback extractive summarization
        
        Args:
            text: Input text
            max_length: Maximum summary length
            
        Returns:
            Dictionary with summary
        """
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 2:
            return {
                'summary': text,
                'method': 'extractive_fallback',
                'original_length': len(text),
                'summary_length': len(text)
            }
        
        # Score sentences
        scored_sentences = self._score_sentences(sentences, text)
        
        # Get top sentences
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:3]
        top_sentences.sort(key=lambda x: sentences.index(x[0]))  # Maintain order
        
        # Build summary
        summary = ' '.join([s[0] for s in top_sentences])
        
        # Truncate if needed
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'
        
        return {
            'summary': summary,
            'method': 'extractive_fallback',
            'original_length': len(text),
            'summary_length': len(summary),
            'compression_ratio': round(len(summary) / len(text) * 100, 2)
        }
    
    def _split_sentences(self, text: str) -> list:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    def _score_sentences(self, sentences: list, text: str) -> list:
        """
        Score sentences based on importance
        
        Args:
            sentences: List of sentences
            text: Full text
            
        Returns:
            List of (sentence, score) tuples
        """
        # Importance keywords
        importance_words = {
            'important': 3, 'key': 3, 'main': 3, 'essential': 3,
            'first': 2, 'second': 2, 'third': 2, 'finally': 2,
            'conclusion': 3, 'summary': 3, 'result': 2, 'therefore': 2,
            'however': 2, 'thus': 2, 'hence': 2, 'because': 2,
            'significant': 3, 'crucial': 3, 'primary': 3, 'fundamental': 3
        }
        
        scored = []
        word_freq = {}
        
        # Calculate word frequency
        words = text.lower().split()
        for word in words:
            word = word.strip('.,!?;:')
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        for sentence in sentences:
            score = 1.0
            words = sentence.lower().split()
            
            # Score based on importance words
            for word in words:
                word_clean = word.strip('.,!?;:')
                if word_clean in importance_words:
                    score += importance_words[word_clean]
                elif word_clean in word_freq:
                    score += word_freq[word_clean] * 0.1
            
            # Boost first and last sentences
            if sentences.index(sentence) == 0:
                score *= 1.5
            if sentences.index(sentence) == len(sentences) - 1:
                score *= 1.3
            
            # Penalize very short sentences
            if len(words) < 10:
                score *= 0.8
            
            scored.append((sentence, score))
        
        return scored
    
    def _clean_summary(self, summary: str) -> str:
        """
        Clean up generated summary
        
        Args:
            summary: Raw summary
            
        Returns:
            Cleaned summary
        """
        # Remove extra spaces
        summary = re.sub(r'\s+', ' ', summary)
        
        # Fix capitalization
        summary = summary.strip()
        if summary and summary[0].islower():
            summary = summary[0].upper() + summary[1:]
        
        # Ensure ends with period
        if summary and summary[-1] not in '.!?':
            summary += '.'
        
        return summary


# Example usage
if __name__ == "__main__":
    sample_text = """
    Machine learning is a subset of artificial intelligence that enables systems 
    to learn and improve from experience without being explicitly programmed. 
    There are three main types of machine learning: supervised learning, 
    unsupervised learning, and reinforcement learning. Supervised learning 
    uses labeled datasets to train algorithms, while unsupervised learning 
    finds patterns in unlabeled data. Reinforcement learning uses rewards 
    and penalties to train agents. Machine learning has applications in 
    image recognition, natural language processing, and recommendation systems.
    """
    
    summarizer = Summarizer(model_name="t5-small")
    result = summarizer.summarize(sample_text, max_length=100)
    
    print("Original:", sample_text[:200], "...")
    print("\nSummary:", result['summary'])
    print("\nMethod:", result['method'])
