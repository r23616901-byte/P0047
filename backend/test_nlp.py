"""
NLP Module Test Script
Tests all NLP components: cleaner, summarizer, keypoints, pipeline
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.cleaner import TextCleaner
from nlp.summarizer import Summarizer
from nlp.keypoints import KeyPointsExtractor
from nlp.pipeline import process_transcript


def test_cleaner():
    """Test text cleaner module"""
    print("\n" + "="*60)
    print("TEST 1: Text Cleaner")
    print("="*60)
    
    sample_text = """
    um so today we are going to discuss uh machine learning basics 
    ah it includes supervised learning and unsupervised learning you know
    like the main difference is that supervised learning uses labeled data
    um whereas unsupervised learning doesn't [laughter]
    well basically these are the two main types okay
    """
    
    cleaner = TextCleaner()
    result = cleaner.clean(sample_text)
    
    print(f"\nOriginal ({result['original_length']} chars):")
    print(f"  {sample_text.strip()[:100]}...")
    
    print(f"\nCleaned ({result['cleaned_length']} chars):")
    print(f"  {result['cleaned_text'][:100]}...")
    
    print(f"\nStatistics:")
    print(f"  Fillers removed: {result['fillers_removed']}")
    print(f"  Noise removed: {result['noise_removed']}")
    print(f"  Reduction: {result['reduction_percentage']}%")
    
    # Assertions
    assert result['fillers_removed'] > 0, "Should remove fillers"
    assert '[laughter]' not in result['cleaned_text'], "Should remove noise"
    assert len(result['cleaned_text']) < len(sample_text), "Should be shorter"
    
    print("\n✅ Cleaner tests passed!")
    return True


def test_summarizer():
    """Test summarizer module"""
    print("\n" + "="*60)
    print("TEST 2: Summarizer")
    print("="*60)
    
    sample_text = """
    Machine learning is a subset of artificial intelligence that enables systems 
    to learn and improve from experience without being explicitly programmed. 
    There are three main types of machine learning: supervised learning, 
    unsupervised learning, and reinforcement learning. Supervised learning 
    uses labeled datasets to train algorithms, while unsupervised learning 
    finds patterns in unlabeled data. Reinforcement learning uses rewards 
    and penalties to train agents. Machine learning has applications in 
    image recognition, natural language processing, and recommendation systems.
    Deep learning is a specialized form using neural networks with multiple layers.
    """
    
    summarizer = Summarizer(model_name="t5-small")
    result = summarizer.summarize(sample_text, max_length=100)
    
    print(f"\nOriginal ({len(sample_text)} chars):")
    print(f"  {sample_text[:150]}...")
    
    print(f"\nSummary ({result['summary_length']} chars):")
    print(f"  {result['summary']}")
    
    print(f"\nMethod: {result['method']}")
    print(f"Compression: {result.get('compression_ratio', 'N/A')}%")
    
    # Assertions
    assert 'summary' in result, "Should have summary"
    assert len(result['summary']) <= len(sample_text), "Summary should be shorter"
    
    print("\n✅ Summarizer tests passed!")
    return True


def test_keypoints():
    """Test key points extractor"""
    print("\n" + "="*60)
    print("TEST 3: Key Points Extractor")
    print("="*60)
    
    sample_text = """
    Machine learning is a subset of artificial intelligence. It enables systems 
    to learn from data without explicit programming. There are three main types: 
    supervised learning, unsupervised learning, and reinforcement learning. 
    Supervised learning uses labeled datasets for training algorithms. 
    Unsupervised learning discovers patterns in unlabeled data. 
    Reinforcement learning uses rewards and penalties for training. 
    Applications include image recognition and natural language processing.
    Deep learning is a specialized form of machine learning using neural networks.
    Neural networks are inspired by biological neural networks in the brain.
    """
    
    extractor = KeyPointsExtractor(num_points=5)
    result = extractor.extract(sample_text)
    
    print(f"\nKey Points ({result['count']} points):")
    for i, point in enumerate(result['key_points'], 1):
        print(f"  {i}. {point}")
    
    print(f"\nMethod: {result['method']}")
    print(f"Total sentences analyzed: {result.get('total_sentences', 'N/A')}")
    
    # Assertions
    assert 'key_points' in result, "Should have key points"
    assert len(result['key_points']) <= 5, "Should have max 5 points"
    assert len(result['key_points']) > 0, "Should have at least 1 point"
    
    print("\n✅ Key points tests passed!")
    return True


def test_pipeline():
    """Test complete NLP pipeline"""
    print("\n" + "="*60)
    print("TEST 4: Complete NLP Pipeline")
    print("="*60)
    
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
    
    result = process_transcript(sample_text)
    
    if result['success']:
        print("\n✅ Pipeline processing successful!")
        
        print(f"\n📝 Cleaned Text Preview:")
        print(f"  {result['cleaned_text'][:150]}...")
        
        print(f"\n📋 Summary:")
        print(f"  {result['summary']}")
        
        print(f"\n📌 Key Points:")
        for i, point in enumerate(result['key_points'], 1):
            print(f"  {i}. {point}")
        
        print(f"\n📊 Statistics:")
        print(f"  Fillers removed: {result['stats']['cleaning']['fillers_removed']}")
        print(f"  Summary method: {result['stats']['summarization']['method']}")
        print(f"  Key points count: {result['stats']['keypoints']['count']}")
        
        # Assertions
        assert result['success'] == True, "Should succeed"
        assert 'cleaned_text' in result, "Should have cleaned text"
        assert 'summary' in result, "Should have summary"
        assert 'key_points' in result, "Should have key points"
        assert len(result['key_points']) > 0, "Should have at least 1 key point"
        
        print("\n✅ Pipeline tests passed!")
        return True
    else:
        print(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")
        return False


def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("TEST 5: Error Handling")
    print("="*60)
    
    # Test empty input
    result = process_transcript("")
    assert result['success'] == False, "Should fail on empty input"
    print("  ✓ Empty input handled correctly")
    
    # Test short input
    result = process_transcript("Hi")
    assert result['success'] == False, "Should fail on short input"
    print("  ✓ Short input handled correctly")
    
    # Test None input
    try:
        result = process_transcript(None)
        print("  ✓ None input handled correctly")
    except Exception as e:
        print(f"  ✓ None input raised exception: {type(e).__name__}")
    
    print("\n✅ Error handling tests passed!")
    return True


def run_all_tests():
    """Run all NLP tests"""
    print("\n" + "="*60)
    print("🧪 NLP MODULE - COMPLETE TEST SUITE")
    print("="*60)
    
    tests = [
        ("Text Cleaner", test_cleaner),
        ("Summarizer", test_summarizer),
        ("Key Points", test_keypoints),
        ("Complete Pipeline", test_pipeline),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n❌ {name} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} ERROR: {str(e)}")
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"  Total Tests: {len(tests)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! NLP Module is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
