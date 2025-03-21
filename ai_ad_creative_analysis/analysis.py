import cv2
import numpy as np
import pytesseract
from PIL import Image

# Image Feature Extraction
def extract_features(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = gray.std()
    text = pytesseract.image_to_string(Image.open(image_path))
    return {"brightness": brightness, "contrast": contrast, "text": text}

# Video Keyframe Extraction
def extract_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    selected_frames = []
    
    for i in range(0, frame_count, max(1, frame_count // 5)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            selected_frames.append(frame)
    cap.release()
    return selected_frames
