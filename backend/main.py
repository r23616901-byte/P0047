from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_services import process_audio
import shutil
import os

app = FastAPI(title="Lecture Summarizer API")

# Configure CORS so the frontend can interact with it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp", exist_ok=True)

@app.post("/api/summarize")
async def summarize_lecture(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Invalid audio format. Please upload a .wav or .mp3 file.")
    
    file_location = f"temp/{file.filename}"
    
    # Save the uploaded file temporarily
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    try:
        # Process the audio file through STT and NLP
        result = process_audio(file_location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

if __name__ == "__main__":
    import uvicorn
    print("Starting backend server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
