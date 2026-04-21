"""
Text Cleaner Module
Removes filler words, normalizes text, and removes noise from transcripts
"""

import re
from typing import Dict, List


class TextCleaner:
    """
    Clean and preprocess raw transcript text
    """
    
    # Filler words to remove (common in spoken language)
    FILLER_WORDS = {
        'um', 'uh', 'ah', 'er', 'ehm', 'em',
        'like', 'you know', 'kind of', 'kinda', 'sort of', 'sorta',
        'basically', 'actually', 'literally', 'obviously',
        'well', 'so', 'okay', 'ok', 'right', 'now',
        'i mean', 'you see', 'you know what',
        'let me see', 'let me think', 'hmm', 'mmm',
        'uhh', 'umm', 'ahh', 'err', 'uhm',
        'gonna', 'wanna', 'gotta', 'dunno', 'cos', 'cause',
        'like i said', 'as i said', 'you know what i mean'
    }
    
    # Noise patterns to remove
    NOISE_PATTERNS = [
        r'\[laughter\]',
        r'\[applause\]',
        r'\[music\]',
        r'\[silence\]',
        r'\[pause\]',
        r'\[crowd noise\]',
        r'\[phone rings\]',
        r'\<.*?\>',  # XML/HTML tags
        r'\(.*?\)',  # Parenthetical notes
        r'\[.*?\]',  # Bracket notes
    ]
    
    def __init__(self):
        """Initialize the text cleaner"""
        self.filler_count = 0
        self.noise_count = 0
        
    def remove_fillers(self, text: str) -> str:
        """
        Remove filler words from text
        
        Args:
            text: Raw transcript text
            
        Returns:
            Text with filler words removed
        """
        words = text.split()
        cleaned_words = []
        i = 0
        
        while i < len(words):
            word = words[i].lower().strip('.,!?;:')
            
            # Check for multi-word fillers
            if i < len(words) - 1:
                two_word = f"{words[i].lower()} {words[i+1].lower()}".strip('.,!?;:')
                if two_word in self.FILLER_WORDS:
                    self.filler_count += 1
                    i += 2
                    continue
            
            if i < len(words) - 2:
                three_word = f"{words[i].lower()} {words[i+1].lower()} {words[i+2].lower()}".strip('.,!?;:')
                if three_word in self.FILLER_WORDS:
                    self.filler_count += 1
                    i += 3
                    continue
            
            # Check single word fillers
            if word not in self.FILLER_WORDS:
                cleaned_words.append(words[i])
            else:
                self.filler_count += 1
            
            i += 1
        
        return ' '.join(cleaned_words)
    
    def remove_noise(self, text: str) -> str:
        """
        Remove noise patterns from text
        
        Args:
            text: Raw transcript text
            
        Returns:
            Text with noise patterns removed
        """
        cleaned_text = text
        
        for pattern in self.NOISE_PATTERNS:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            self.noise_count += len(matches)
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text (lowercase, spacing, punctuation)
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase (optional - keep for consistency)
        # text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.,!?;:])\1+', r'\1', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def clean(self, text: str, aggressive: bool = False) -> Dict:
        """
        Complete text cleaning pipeline
        
        Args:
            text: Raw transcript text
            aggressive: If True, apply more aggressive cleaning
            
        Returns:
            Dictionary with cleaned text and statistics
        """
        if not text:
            return {
                'success': False,
                'error': 'Empty input text',
                'cleaned_text': '',
                'stats': {}
            }
        
        # Reset counters
        self.filler_count = 0
        self.noise_count = 0
        
        original_length = len(text)
        
        # Step 1: Remove noise
        cleaned = self.remove_noise(text)
        
        # Step 2: Remove fillers
        cleaned = self.remove_fillers(cleaned)
        
        # Step 3: Normalize
        cleaned = self.normalize_text(cleaned)
        
        # Aggressive cleaning (optional)
        if aggressive:
            # Remove very short words (except 'I', 'a')
            words = cleaned.split()
            words = [w for w in words if len(w) > 1 or w.lower() in ['i', 'a']]
            cleaned = ' '.join(words)
        
        cleaned_length = len(cleaned)
        
        return {
            'success': True,
            'cleaned_text': cleaned,
            'stats': {
                'original_length': original_length,
                'cleaned_length': cleaned_length,
                'reduction': original_length - cleaned_length,
                'fillers_removed': self.filler_count,
                'noise_removed': self.noise_count
            }
        }
