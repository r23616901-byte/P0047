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
                'key_points': [s.rstrip('.') + '.' for s in sentences],
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
            # Add more from sentences
            for sentence in sentences:
                formatted = self._format_point(sentence)
                if formatted not in unique_points and len(formatted) > 20:
                    unique_points.append(formatted)
                if len(unique_points) >= self.num_points:
                    break
        
        return {
            'key_points': unique_points[:self.num_points],
            'method': 'tfidf_textrank_hybrid',
            'count': len(unique_points[:self.num_points]),
            'total_sentences': len(sentences)
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    def _extract_tfidf(self, sentences: List[str], text: str) -> List[Tuple[str, float]]:
        """
        Extract key points using TF-IDF scoring
        
        Args:
            sentences: List of sentences
            text: Full text
            
        Returns:
            List of (sentence, score) tuples
        """
        # Calculate term frequency for each sentence
        sentence_scores = []
        
        # Get all words from text
        all_words = text.lower().split()
        all_words = [w.strip('.,!?;:"\'') for w in all_words if len(w) > 2]
        
        # Calculate document frequency
        word_doc_freq = Counter()
        for sentence in sentences:
            words = set(sentence.lower().split())
            words = {w.strip('.,!?;:"\'') for w in words if len(w) > 2}
            for word in words:
                word_doc_freq[word] += 1
        
        # Score each sentence
        for sentence in sentences:
            words = sentence.lower().split()
            words = [w.strip('.,!?;:"\'') for w in words if len(w) > 2 and w not in self.stopwords]
            
            if not words:
                continue
            
            # TF-IDF score
            tfidf_score = 0
            for word in words:
                tf = words.count(word) / len(words)
                idf = len(sentences) / (word_doc_freq.get(word, 1) + 1)
                tfidf_score += tf * idf
            
            # Normalize by sentence length
            tfidf_score /= len(words)
            
            # Boost important positions
            if sentences.index(sentence) == 0:
                tfidf_score *= 1.5
            if sentences.index(sentence) == len(sentences) - 1:
                tfidf_score *= 1.3
            
            sentence_scores.append((sentence, tfidf_score))
        
        # Sort by score
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        return sentence_scores
    
    def _extract_textrank(self, sentences: List[str]) -> List[Tuple[str, float]]:
        """
        Extract key points using simplified TextRank algorithm
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of (sentence, score) tuples
        """
        if len(sentences) < 3:
            return [(s, 1.0) for s in sentences]
        
        # Initialize scores
        scores = {i: 1.0 for i in range(len(sentences))}
        
        # Build similarity matrix
        similarity_matrix = [[0.0] * len(sentences) for _ in range(len(sentences))]
        
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                similarity = self._sentence_similarity(sentences[i], sentences[j])
                similarity_matrix[i][j] = similarity
                similarity_matrix[j][i] = similarity
        
        # Run PageRank-like algorithm
        damping = 0.85
        iterations = 30
        
        for _ in range(iterations):
            new_scores = {}
            for i in range(len(sentences)):
                rank = (1 - damping)
                for j in range(len(sentences)):
                    if i != j and similarity_matrix[i][j] > 0:
                        sum_sim = sum(similarity_matrix[j])
                        if sum_sim > 0:
                            rank += damping * (similarity_matrix[i][j] / sum_sim) * scores[j]
                new_scores[i] = rank
            scores = new_scores
        
        # Convert to list of tuples
        scored_sentences = [(sentences[i], score) for i, score in scores.items()]
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        return scored_sentences
    
    def _sentence_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate similarity between two sentences
        
        Args:
            s1: First sentence
            s2: Second sentence
            
        Returns:
            Similarity score (0-1)
        """
        words1 = set(s1.lower().split())
        words1 = {w.strip('.,!?;:"\'') for w in words1 if len(w) > 2 and w not in self.stopwords}
        
        words2 = set(s2.lower().split())
        words2 = {w.strip('.,!?;:"\'') for w in words2 if len(w) > 2 and w not in self.stopwords}
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _combine_and_deduplicate(self, tfidf: List, textrank: List) -> List[str]:
        """
        Combine results from both algorithms and deduplicate
        
        Args:
            tfidf: TF-IDF scored sentences
            textrank: TextRank scored sentences
            
        Returns:
            Combined list of unique sentences
        """
        # Take top from each
        top_tfidf = [s[0] for s in tfidf[:self.num_points * 2]]
        top_textrank = [s[0] for s in textrank[:self.num_points * 2]]
        
        # Combine with alternating selection
        combined = []
        seen = set()
        
        for i in range(max(len(top_tfidf), len(top_textrank))):
            if i < len(top_tfidf):
                sentence = top_tfidf[i].strip()
                if sentence.lower() not in seen:
                    combined.append(sentence)
                    seen.add(sentence.lower())
            
            if i < len(top_textrank):
                sentence = top_textrank[i].strip()
                if sentence.lower() not in seen:
                    combined.append(sentence)
                    seen.add(sentence.lower())
        
        return combined
    
    def _format_point(self, point: str) -> str:
        """
        Format a key point for display
        
        Args:
            point: Raw sentence
            
        Returns:
            Formatted key point
        """
        point = point.strip()
        
        # Remove leading/trailing punctuation
        point = point.strip('.,!?;:"\' ')
        
        # Capitalize first letter
        if point:
            point = point[0].upper() + point[1:]
        
        # Ensure ends with period
        if point and point[-1] not in '.!?':
            point += '.'
        
        # Truncate if too long
        if len(point) > 200:
            point = point[:197] + '...'
        
        return point
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> Dict:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            num_keywords: Number of keywords to extract
            
        Returns:
            Dictionary with keywords
        """
        words = text.lower().split()
        words = [w.strip('.,!?;:"\'') for w in words if len(w) > 3 and w not in self.stopwords]
        
        word_freq = Counter(words)
        top_keywords = word_freq.most_common(num_keywords)
        
        return {
            'keywords': [kw[0] for kw in top_keywords],
            'keyword_scores': dict(top_keywords),
            'count': len(top_keywords)
        }


# Example usage
if __name__ == "__main__":
    sample_text = """
    Machine learning is a subset of artificial intelligence. It enables systems 
    to learn from data without explicit programming. There are three main types: 
    supervised learning, unsupervised learning, and reinforcement learning. 
    Supervised learning uses labeled datasets for training algorithms. 
    Unsupervised learning discovers patterns in unlabeled data. 
    Reinforcement learning uses rewards and penalties for training. 
    Applications include image recognition and natural language processing.
    Deep learning is a specialized form of machine learning using neural networks.
    """
    
    extractor = KeyPointsExtractor(num_points=5)
    result = extractor.extract(sample_text)
    
    print("Key Points:")
    for i, point in enumerate(result['key_points'], 1):
        print(f"  {i}. {point}")
    print(f"\nMethod: {result['method']}")
