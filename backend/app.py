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
        'name': 'AI-Based Lecture Summarizer - Audio to Text API',
        'version': '1.0.0',
        'endpoints': {
            'POST /transcribe': 'Upload audio file and get transcript',
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
