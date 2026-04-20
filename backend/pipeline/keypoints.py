"""
Key Points Extraction Module
Extracts important bullet points from text using TF-IDF and TextRank
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class KeyPointsExtractor:
    """
    Extract key points from text using multiple algorithms
    """
    
    def __init__(self, num_points: int = 5):
        """
        Initialize the key points extractor
        
        Args:
            num_points: Number of key points to extract
        """
        self.num_points = num_points
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """Load common English stopwords"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
            'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here',
            'there', 'then', 'once', 'if', 'because', 'as', 'until', 'while',
            'about', 'against', 'between', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under'
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Split on common sentence endings
        sentences = re.split(r'[.!?]+', text)
        # Filter empty and very short sentences
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        return sentences
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-z]+\b', text.lower())
        # Remove stopwords
        words = [w for w in words if w not in self.stopwords]
        return words
    
    def _extract_tfidf(self, sentences: List[str], full_text: str) -> List[Tuple[str, float]]:
        """
        Extract key points using TF-IDF scoring
        
        Args:
            sentences: List of sentences
            full_text: Original full text
            
        Returns:
            List of (sentence, score) tuples
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            if len(sentences) < 2:
                return [(s, 1.0) for s in sentences]
            
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                stop_words=list(self.stopwords),
                max_features=1000,
                ngram_range=(1, 2)
            )
            
            # Fit and transform
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Calculate sentence scores (sum of TF-IDF values)
            scores = tfidf_matrix.sum(axis=1).A1
            
            # Pair sentences with scores
            scored_sentences = list(zip(sentences, scores))
            
            # Sort by score (descending)
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            
            return scored_sentences
            
        except ImportError:
            print("scikit-learn not available, using fallback method")
            return self._extract_frequency(sentences)
        except Exception as e:
            print(f"TF-IDF error: {e}")
            return self._extract_frequency(sentences)
    
    def _extract_frequency(self, sentences: List[str]) -> List[Tuple[str, float]]:
        """
        Fallback: Extract key points using word frequency
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of (sentence, score) tuples
        """
        # Count word frequencies
        all_words = []
        for sentence in sentences:
            all_words.extend(self._tokenize(sentence))
        
        word_freq = Counter(all_words)
        
        # Score sentences
        scored_sentences = []
        for sentence in sentences:
            words = self._tokenize(sentence)
            score = sum(word_freq.get(w, 0) for w in words)
            # Normalize by sentence length
            score = score / max(len(words), 1)
            scored_sentences.append((sentence, score))
        
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return scored_sentences
    
    def _extract_textrank(self, sentences: List[str]) -> List[Tuple[str, float]]:
        """
        Extract key points using TextRank-like algorithm
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of (sentence, score) tuples
        """
        try:
            # Try to use RAKE
            from rake_nltk import Rake
            
            rake = Rake(stopwords=list(self.stopwords))
            rake.extract_keywords_from_text(' '.join(sentences))
            
            # Get ranked phrases
            ranked_phrases = rake.get_ranked_phrases()
            
            # Score sentences based on ranked phrases
            scored_sentences = []
            for sentence in sentences:
                score = 0
                sentence_lower = sentence.lower()
                for phrase in ranked_phrases[:20]:  # Top 20 phrases
                    if phrase in sentence_lower:
                        score += 1
                scored_sentences.append((sentence, score))
            
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            return scored_sentences
            
        except ImportError:
            print("rake-nltk not available, using TF-IDF instead")
            return self._extract_tfidf(sentences)
        except Exception as e:
            print(f"TextRank error: {e}")
            return self._extract_tfidf(sentences)
    
    def _combine_and_deduplicate(self, tfidf_points: List[Tuple[str, float]], 
                                   textrank_points: List[Tuple[str, float]]) -> List[str]:
        """
        Combine results from both algorithms and deduplicate
        
        Args:
            tfidf_points: TF-IDF scored sentences
            textrank_points: TextRank scored sentences
            
        Returns:
            Combined and deduplicated list of sentences
        """
        # Take top from each
        top_tfidf = [s for s, _ in tfidf_points[:self.num_points]]
        top_textrank = [s for s, _ in textrank_points[:self.num_points]]
        
        # Combine
        combined = top_tfidf + top_textrank
        
        # Deduplicate (case-insensitive)
        seen = set()
        unique = []
        for sentence in combined:
            key = sentence.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(sentence)
        
        return unique
    
    def _format_point(self, point: str) -> str:
        """
        Format a key point for display
        
        Args:
            point: Raw sentence
            
        Returns:
            Formatted key point
        """
        # Clean up
        point = point.strip()
        
        # Ensure it ends with proper punctuation
        if not point[-1] in '.!?':
            point += '.'
        
        # Capitalize first letter
        point = point[0].upper() + point[1:] if point else point
        
        # Limit length
        if len(point) > 200:
            point = point[:197] + '...'
        
        return point
    
    def extract(self, text: str, num_points: int = None) -> Dict:
        """
        Extract key points from text
        
        Args:
            text: Input text
            num_points: Override default number of points
            
        Returns:
            Dictionary with key points and metadata
        """
        if num_points:
            self.num_points = num_points
        
        if not text or len(text.strip()) < 100:
            return {
                'key_points': [],
                'method': 'empty_input',
                'count': 0
            }
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) < self.num_points:
            # Not enough sentences, return what we have
            return {
                'key_points': [self._format_point(s) for s in sentences],
                'method': 'all_sentences',
                'count': len(sentences)
            }
        
        # Try TF-IDF first
        tfidf_points = self._extract_tfidf(sentences, text)
        
        # Try TextRank as alternative
        textrank_points = self._extract_textrank(sentences)
        
        # Combine and deduplicate
        combined = self._combine_and_deduplicate(tfidf_points, textrank_points)
        
        # Select top points
        top_points = combined[:self.num_points]
        
        # Format points
        formatted_points = [self._format_point(p) for p in top_points]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_points = []
        for point in formatted_points:
            point_lower = point.lower()
            if point_lower not in seen and len(point) > 20:
                seen.add(point_lower)
                unique_points.append(point)
        
        # Ensure we have enough points
        if len(unique_points) < self.num_points:
            # Add more from original sentences
            for sentence in sentences:
                formatted = self._format_point(sentence)
                if formatted not in unique_points and len(unique_points) < self.num_points:
                    unique_points.append(formatted)
        
        return {
            'key_points': unique_points[:self.num_points],
            'method': 'tfidf_textrank_combined',
            'count': len(unique_points[:self.num_points]),
            'total_sentences': len(sentences)
        }
