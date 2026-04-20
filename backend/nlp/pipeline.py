"""
NLP Pipeline Module
Integrates text cleaning, summarization, and key points extraction
"""

from typing import Dict, Optional
from .cleaner import TextCleaner
from .summarizer import Summarizer
from .keypoints import KeyPointsExtractor


class NLPPipeline:
    """
    Complete NLP pipeline for lecture transcript processing
    """
    
    def __init__(
        self,
        summarizer_model: str = "t5-small",
        num_key_points: int = 5
    ):
        """
        Initialize the NLP pipeline
        
        Args:
            summarizer_model: T5 model name for summarization
            num_key_points: Number of key points to extract
        """
        self.cleaner = TextCleaner()
        self.summarizer = Summarizer(model_name=summarizer_model)
        self.keypoints_extractor = KeyPointsExtractor(num_points=num_key_points)
        
        self._initialized = False
    
    def process(self, text: str, aggressive_cleaning: bool = False) -> Dict:
        """
        Process transcript through complete NLP pipeline
        
        Args:
            text: Raw transcript text
            aggressive_cleaning: If True, apply more aggressive cleaning
            
        Returns:
            Dictionary with all processed outputs
        """
        if not text or len(text.strip()) < 10:
            return {
                'success': False,
                'error': 'Input text is too short or empty',
                'cleaned_text': '',
                'summary': '',
                'key_points': [],
                'stats': {}
            }
        
        result = {
            'success': True,
            'stats': {}
        }
        
        # Step 1: Clean the text
        print("Step 1: Cleaning text...")
        clean_result = self.cleaner.clean(text, aggressive=aggressive_cleaning)
        result['cleaned_text'] = clean_result['cleaned_text']
        result['stats']['cleaning'] = {
            'original_length': clean_result['original_length'],
            'cleaned_length': clean_result['cleaned_length'],
            'fillers_removed': clean_result['fillers_removed'],
            'noise_removed': clean_result['noise_removed']
        }
        
        # Step 2: Generate summary
        print("Step 2: Generating summary...")
        summary_result = self.summarizer.summarize(
            result['cleaned_text'],
            max_length=150,
            min_length=40
        )
        result['summary'] = summary_result['summary']
        result['stats']['summarization'] = {
            'method': summary_result.get('method', 'unknown'),
            'summary_length': summary_result.get('summary_length', 0),
            'compression_ratio': summary_result.get('compression_ratio', 0)
        }
        
        # Step 3: Extract key points
        print("Step 3: Extracting key points...")
        keypoints_result = self.keypoints_extractor.extract(
            result['cleaned_text'],
            num_points=5
        )
        result['key_points'] = keypoints_result['key_points']
        result['stats']['keypoints'] = {
            'method': keypoints_result.get('method', 'unknown'),
            'count': keypoints_result.get('count', 0)
        }
        
        # Overall stats
        result['stats']['overall'] = {
            'input_length': len(text),
            'output_summary_length': len(result['summary']),
            'output_keypoints_count': len(result['key_points']),
            'processing_complete': True
        }
        
        print("NLP Pipeline completed successfully!")
        return result
    
    def process_text_only(self, text: str) -> Dict:
        """
        Process text without full pipeline (for quick testing)
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with cleaned text only
        """
        clean_result = self.cleaner.clean(text)
        return {
            'success': True,
            'cleaned_text': clean_result['cleaned_text'],
            'stats': {
                'fillers_removed': clean_result['fillers_removed'],
                'noise_removed': clean_result['noise_removed']
            }
        }
    
    def summarize_only(self, text: str, max_length: int = 150) -> Dict:
        """
        Generate summary only
        
        Args:
            text: Input text
            max_length: Maximum summary length
            
        Returns:
            Dictionary with summary
        """
        clean_result = self.cleaner.clean(text)
        summary_result = self.summarizer.summarize(
            clean_result['cleaned_text'],
            max_length=max_length
        )
        return {
            'success': True,
            'summary': summary_result['summary'],
            'method': summary_result.get('method', 'unknown'),
            'stats': {
                'summary_length': summary_result.get('summary_length', 0)
            }
        }
    
    def extract_keypoints_only(self, text: str, num_points: int = 5) -> Dict:
        """
        Extract key points only
        
        Args:
            text: Input text
            num_points: Number of key points
            
        Returns:
            Dictionary with key points
        """
        clean_result = self.cleaner.clean(text)
        keypoints_result = self.keypoints_extractor.extract(
            clean_result['cleaned_text'],
            num_points=num_points
        )
        return {
            'success': True,
            'key_points': keypoints_result['key_points'],
            'count': keypoints_result.get('count', 0),
            'method': keypoints_result.get('method', 'unknown')
        }
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> Dict:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            num_keywords: Number of keywords
            
        Returns:
            Dictionary with keywords
        """
        clean_result = self.cleaner.clean(text)
        keywords_result = self.keypoints_extractor.extract_keywords(
            clean_result['cleaned_text'],
            num_keywords=num_keywords
        )
        return {
            'success': True,
            'keywords': keywords_result['keywords'],
            'keyword_scores': keywords_result.get('keyword_scores', {}),
            'count': keywords_result.get('count', 0)
        }


# Convenience function for quick usage
def process_transcript(
    text: str,
    model_name: str = "t5-small",
    num_key_points: int = 5,
    aggressive_cleaning: bool = False
) -> Dict:
    """
    Process transcript through NLP pipeline
    
    Args:
        text: Raw transcript text
        model_name: T5 model name
        num_key_points: Number of key points
        aggressive_cleaning: Cleaning intensity
        
    Returns:
        Dictionary with processed output
    """
    pipeline = NLPPipeline(
        summarizer_model=model_name,
        num_key_points=num_key_points
    )
    return pipeline.process(text, aggressive_cleaning=aggressive_cleaning)


# Example usage
if __name__ == "__main__":
    sample_text = """
    um so today we are going to discuss uh machine learning basics 
    ah it includes supervised learning and unsupervised learning you know
    like the main difference is that supervised learning uses labeled data
    um whereas unsupervised learning doesn't [laughter]
    well basically these are the two main types okay
    supervised learning is used for classification and regression tasks
    while unsupervised learning is used for clustering and dimensionality reduction
    deep learning is a subset of machine learning that uses neural networks
    it has become very popular for image and speech recognition tasks
    the future of machine learning looks very promising with many applications
    """
    
    print("=" * 60)
    print("NLP Pipeline Test")
    print("=" * 60)
    
    result = process_transcript(sample_text)
    
    if result['success']:
        print("\n📝 CLEANED TEXT:")
        print(result['cleaned_text'][:200] + "..." if len(result['cleaned_text']) > 200 else result['cleaned_text'])
        
        print("\n📋 SUMMARY:")
        print(result['summary'])
        
        print("\n📌 KEY POINTS:")
        for i, point in enumerate(result['key_points'], 1):
            print(f"  {i}. {point}")
        
        print("\n📊 STATS:")
        print(f"  Fillers removed: {result['stats']['cleaning']['fillers_removed']}")
        print(f"  Summary method: {result['stats']['summarization']['method']}")
        print(f"  Key points count: {result['stats']['keypoints']['count']}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
