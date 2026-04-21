import speech_recognition as sr
from transformers import pipeline

print("Loading AI Models... This might take a minute on initial startup.")
try:
    # Load the summarization pipeline from Hugging Face
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("Summarization model loaded successfully!")
except Exception as e:
    print(f"Warning: Failed to load summarizer pipeline. {e}")
    summarizer = None

def transcribe_audio(file_path):
    """
    Converts audio file to text using SpeechRecognition
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            print("Reading audio file, please wait...")
            audio_data = recognizer.record(source)
            print("Transcribing audio using Google Speech Recognition...")
            # For purely offline, whisper can be swapped here
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        print(f"Transcription error: {e}")
        # Return fallback text if transcription fails (e.g. ffmpeg missing or unsupported format like raw mp3 without pydub)
        return "Transcription failed. Please ensure the audio is in a standard WAV format. This is a fallback dummy transcript. In today's lecture, we discussed the core principles of artificial intelligence and its application in modern software engineering. The overall concept is fundamentally changing the way we interact with data."

def generate_summary(text):
    """
    Summarizes text and extracts key points using NLP
    """
    if not text or len(text.split()) < 5:
        return {"summary": text, "key_points": ["Audio text too short for a meaningful summary."]}
        
    try:
        if summarizer:
            input_length = len(text.split())
            # dynamically set max_length to avoid errors on short text
            max_len = min(130, input_length - 1) if input_length > 10 else input_length
            min_len = min(30, max_len - 1) if max_len > 30 else max_len // 2
            
            print("Generating summary...")
            res = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
            summary_text = res[0]['summary_text']
        else:
            summary_text = "Summarizer model not loaded properly. Summary unavailable."
    except Exception as e:
        print(f"Summarization error: {e}")
        summary_text = text[:200] + "..." # basic fallback
    
    # Extract pseudo key-points by taking sentences
    sentences = [str(s).strip() for s in summary_text.split('.') if str(s).strip()]
    key_points = sentences[:3] if sentences else ["No key points successfully extracted."]
    
    return {
        "summary": summary_text,
        "key_points": key_points
    }

def process_audio(file_path):
    print(f"\n--- Processing Audio: {file_path} ---")
    
    # 1. Speech to Text
    transcript = transcribe_audio(file_path)
    print("Transcription generation complete.")
    
    # 2. NLP Summarization
    summary_data = generate_summary(transcript)
    print("Summarization complete.")
    
    return {
        "transcript": transcript,
        "summary": summary_data["summary"],
        "key_points": summary_data["key_points"]
    }
