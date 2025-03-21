from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import uvicorn
import shutil
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from database import SessionLocal, PerformanceData
from analysis import extract_features, extract_video_frames
from visualization import generate_visualization

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File Upload Endpoint
@app.post("/upload")
def upload_file(file: UploadFile = File(...), ctr: float = Form(...), conversion_rate: float = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()
    db.add(PerformanceData(filename=file.filename, ctr=ctr, conversion_rate=conversion_rate))
    db.commit()
    db.close()
    
    return {"message": "File uploaded successfully", "filename": file.filename}

# Analysis Endpoint
@app.get("/analysis")
def analyze():
    results = {}
    db = SessionLocal()
    data_entries = db.query(PerformanceData).all()
    db.close()

    for entry in data_entries:
        file_path = os.path.join(UPLOAD_DIR, entry.filename)
        if entry.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            features = extract_features(file_path)
        elif entry.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            frames = extract_video_frames(file_path)
            features = [extract_features(frame) for frame in frames]
        else:
            continue

        results[entry.filename] = {"features": features, "performance": {"ctr": entry.ctr, "conversion_rate": entry.conversion_rate}}
    return results

# Correlation & Visualization
@app.get("/correlation")
def correlation():
    return generate_visualization()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
