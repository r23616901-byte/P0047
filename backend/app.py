"""
AI-Based Lecture Summarizer - Audio to Text Module
Backend Server using Flask and OpenAI Whisper
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import tempfile
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load Whisper model (using 'base' for good balance of speed and accuracy)
# Options: tiny, base, small, medium, large
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded successfully!")

# Configure upload settings
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """Get file extension from filename"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_summary(transcript):
    """Generate a summary from transcript using extractive summarization"""
    if not transcript or len(transcript) < 100:
        return transcript
    
    # Split into sentences
    sentences = [s.strip() for s in transcript.replace('!', '.').replace('?', '.').split('.') if s.strip() and len(s.strip()) > 20]
    
    if len(sentences) <= 2:
        return transcript
    
    # Simple extractive summary: take key sentences
    summary_sentences = []
    
    # First sentence (introduction)
    summary_sentences.append(sentences[0])
    
    # Middle sentences (key content)
    mid_point = len(sentences) // 2
    if len(sentences) > 3:
        summary_sentences.append(sentences[mid_point])
        if len(sentences) > 5:
            summary_sentences.append(sentences[mid_point + 1])
    
    # Last sentence (conclusion)
    if len(sentences) > 1:
        summary_sentences.append(sentences[-1])
    
    return '. '.join(summary_sentences) + '.'

def extract_key_points(transcript):
    """Extract key points from transcript"""
    if not transcript:
        return []
    
    # Keywords indicating important information
    importance_keywords = [
        'important', 'key', 'remember', 'note', 'essential',
        'first', 'second', 'third', 'finally', 'next',
        'in conclusion', 'to summarize', 'main point',
        'crucial', 'significant', 'primarily', 'mainly',
        'the main', 'this is', 'we will', 'today we'
    ]
    
    # Split into sentences
    sentences = [s.strip() for s in transcript.replace('!', '.').replace('?', '.').split('.') if s.strip() and len(s.strip()) > 25]
    
    key_points = []
    
    # Find sentences with importance keywords
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for keyword in importance_keywords:
            if keyword in sentence_lower:
                clean_point = sentence.rstrip('.') + '.'
                if clean_point not in key_points:
                    key_points.append(clean_point)
                break
    
    # If not enough key points, take longest/most informative sentences
    if len(key_points) < 4:
        sorted_sentences = sorted(sentences, key=len, reverse=True)
        for sentence in sorted_sentences[:7]:
            clean_point = sentence.rstrip('.') + '.'
            if clean_point not in key_points:
                key_points.append(clean_point)
            if len(key_points) >= 7:
                break
    
    return key_points[:7]  # Return max 7 key points

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint to transcribe audio file to text using Whisper
    
    Request:
        - audio: Audio file (multipart/form-data)
    
    Response:
        - success: boolean
        - transcript: string (if successful)
        - error: string (if failed)
    """
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided. Please upload an audio file.'
            }), 400
        
        file = request.files['audio']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected. Please choose an audio file.'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Unsupported file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end of file
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 400
        
        # Create temporary file to save audio
        extension = get_file_extension(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}')
        temp_filename = temp_file.name
        
        try:
            # Save uploaded file
            file.save(temp_filename)
            
            # Transcribe audio using Whisper
            print(f"Transcribing audio file: {file.filename}")
            result = model.transcribe(temp_filename)
            transcript = result['text'].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            # Return successful response
            return jsonify({
                'success': True,
                'transcript': transcript,
                'language': result.get('language', 'unknown'),
                'duration': result.get('segments', [{}])[-1].get('end', 0) if result.get('segments') else 0
            })
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise e
            
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Transcription failed: {str(e)}'
        }), 500

@app.route('/summarize', methods=['POST'])
def summarize_audio():
    """
    Endpoint to transcribe audio and generate summary with key points
    
    Request:
        - audio: Audio file (multipart/form-data)
    
    Response:
        - success: boolean
        - transcript: string (full transcription)
        - summary: string (condensed summary)
        - key_points: list (important points from lecture)
    """
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided. Please upload an audio file.'
            }), 400
        
        file = request.files['audio']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected. Please choose an audio file.'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Unsupported file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 400
        
        # Create temporary file
        extension = get_file_extension(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}')
        temp_filename = temp_file.name
        
        try:
            # Save uploaded file
            file.save(temp_filename)
            
            # Transcribe audio using Whisper
            print(f"Processing audio file: {file.filename}")
            result = model.transcribe(temp_filename)
            transcript = result['text'].strip()
            
            # Generate summary
            summary = generate_summary(transcript)
            
            # Extract key points
            key_points = extract_key_points(transcript)
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            print("✅ Processing complete!")
            
            # Return successful response
            return jsonify({
                'success': True,
                'transcript': transcript,
                'summary': summary,
                'key_points': key_points,
                'language': result.get('language', 'unknown'),
                'duration': result.get('segments', [{}])[-1].get('end', 0) if result.get('segments') else 0
            })
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise e
            
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'whisper-base',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API info"""
    return jsonify({
        'name': 'AI-Based Lecture Summarizer - Full API',
        'version': '2.0.0',
        'endpoints': {
            'POST /transcribe': 'Upload audio file and get transcript',
            'POST /summarize': 'Upload audio file and get transcript + summary + key points',
            'GET /health': 'Health check endpoint'
        },
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': f'{MAX_FILE_SIZE // (1024*1024)}MB'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("AI-Based Lecture Summarizer - Audio to Text Server")
    print("=" * 60)
    print(f"Supported formats: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"Max file size: {MAX_FILE_SIZE // (1024*1024)}MB")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
