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
        Normalize text: lowercase, remove extra spaces, fix punctuation
        
        Args:
            text: Raw transcript text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase (optional - can keep original case)
        # text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s*', r'\1 ', text)
        
        # Remove repeated words
        text = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', text, flags=re.IGNORECASE)
        
        # Fix common speech patterns
        text = re.sub(r'\bi\b', 'I', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_special_characters(self, text: str) -> str:
        """
        Remove unnecessary special characters while keeping punctuation
        
        Args:
            text: Raw transcript text
            
        Returns:
            Text with special characters removed
        """
        # Keep letters, numbers, basic punctuation and spaces
        text = re.sub(r'[^\w\s.,!?;:\'\"]+', '', text)
        return text
    
    def clean(self, text: str, aggressive: bool = False) -> Dict:
        """
        Full cleaning pipeline
        
        Args:
            text: Raw transcript text
            aggressive: If True, apply more aggressive cleaning
            
        Returns:
            Dictionary with cleaned text and statistics
        """
        # Reset counters
        self.filler_count = 0
        self.noise_count = 0
        
        original_length = len(text)
        
        # Step 1: Remove noise patterns
        cleaned = self.remove_noise(text)
        
        # Step 2: Remove filler words
        cleaned = self.remove_fillers(cleaned)
        
        # Step 3: Normalize text
        cleaned = self.normalize_text(cleaned)
        
        # Step 4: Remove special characters (if aggressive)
        if aggressive:
            cleaned = self.remove_special_characters(cleaned)
        
        # Step 5: Final normalization
        cleaned = self.normalize_text(cleaned)
        
        cleaned_length = len(cleaned)
        
        return {
            'cleaned_text': cleaned,
            'original_length': original_length,
            'cleaned_length': cleaned_length,
            'fillers_removed': self.filler_count,
            'noise_removed': self.noise_count,
            'reduction_percentage': round((1 - cleaned_length / original_length) * 100, 2) if original_length > 0 else 0
        }
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Cleaned text
            
        Returns:
            List of sentences
        """
        # Split on sentence-ending punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Filter empty and very short sentences
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return sentences


# Example usage
if __name__ == "__main__":
    sample_text = """
    um so today we are going to discuss uh machine learning basics 
    ah it includes supervised learning and unsupervised learning you know
    like the main difference is that supervised learning uses labeled data
    um whereas unsupervised learning doesn't [laughter]
    well basically these are the two main types okay
    """
    
    cleaner = TextCleaner()
    result = cleaner.clean(sample_text)
    
    print("Original:", sample_text)
    print("\nCleaned:", result['cleaned_text'])
    print("\nStats:", {k: v for k, v in result.items() if k != 'cleaned_text'})
