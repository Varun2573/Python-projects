import os
import shutil
import cv2
import base64
import gridfs
import pymongo
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from twilio.rest import Client
import time

# Load API keys and Twilio credentials
load_dotenv()
API_KEY = os.getenv("gemini_api_key")
TWILIO_SID = os.getenv("twilio_sid")
TWILIO_AUTH_TOKEN = os.getenv("twilio_auth_token")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
USER_PHONE_NUMBER = os.getenv("USER_PHONE_NUMBER")

# Configure Gemini AI
genai.configure(api_key=API_KEY)

# Initialize FastAPI
app = FastAPI()

# Setup MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["MajorProject"]
fs = gridfs.GridFS(db)

# Setup Templates
templates = Jinja2Templates(directory="templates")

# Setup Twilio client
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


# Function to extract key frames
def extract_key_frames(video_path, output_folder, frame_interval=5):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    extracted_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % int(fps * frame_interval) == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
        frame_count += 1

    cap.release()
    return extracted_frames


# Function to encode images as base64
def encode_images(image_paths):
    encoded_images = []
    for img_path in image_paths:
        with open(img_path, "rb") as img_file:
            encoded_images.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_file.read()).decode("utf-8")
            })
    return encoded_images


# Function to detect crime type
def detect_crime_type(video_path):
    frames_folder = "frames"
    key_frames = extract_key_frames(video_path, frames_folder)

    if not key_frames:
        return "No Crime Detected"

    model = genai.GenerativeModel("gemini-1.5-pro")
    images_data = encode_images(key_frames)

    prompt_text = """
    Based on these images, identify the crime type in one word only.
    Options: 'Theft', 'Robbery', 'Assault', 'Vandalism', 'Arson', 'Murder', 'No Crime'.
    Do not provide any explanation.
    """

    try:
        response = model.generate_content([
            {"role": "user", "parts": images_data + [{"text": prompt_text}]}
        ])
        crime_type = response.text.strip() if response else "Unknown"
        return crime_type
    except Exception as e:
        return f"Error: {str(e)}"


# Function to send Twilio alert
def send_alert(crime_type, video_id):
    message_body = f"🚨 ALERT: A crime ({crime_type}) has been detected! Video ID: {video_id}"
    twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=USER_PHONE_NUMBER
    )


# Route: Serve HTML Template
@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route: Handle Video Upload & Crime Detection
@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"uploads/{file.filename}"

    # Save video file
    os.makedirs("uploads", exist_ok=True)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect crime type
    crime_type = detect_crime_type(video_path)

    # If crime is detected, store video in MongoDB
    if crime_type.lower() != "no crime":
        with open(video_path, "rb") as video_file:
            video_id = fs.put(video_file, filename=file.filename)

        # Send Twilio alert
        send_alert(crime_type, video_id)

        return JSONResponse(content={"message": "Crime detected! Video stored.", "crime_type": crime_type, "video_id": str(video_id)})

    return JSONResponse(content={"message": "No crime detected, video not stored.", "crime_type": crime_type})


# Route: Real-Time Detection with Camera Preview
@app.get("/detect-real-time/")
async def detect_real_time():
    video_path = "uploads/realtime_capture.avi"
    os.makedirs("uploads", exist_ok=True)

    cap = cv2.VideoCapture(0)  # Open webcam
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, 10.0, (640, 480))

    start_time = time.time()
    while time.time() - start_time < 10:  # Record for 10 seconds
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    # Detect crime
    crime_type = detect_crime_type(video_path)

    # If crime detected, store video & alert
    if crime_type.lower() != "no crime":
        with open(video_path, "rb") as video_file:
            video_id = fs.put(video_file, filename="realtime_capture.avi")
        send_alert(crime_type, video_id)
        return JSONResponse(content={"message": "Crime detected in real-time!", "crime_type": crime_type, "video_id": str(video_id)})

    return JSONResponse(content={"message": "No crime detected in real-time.", "crime_type": crime_type})


# Route: Stream Camera Preview
@app.get("/camera-feed/")
def camera_feed():
    cap = cv2.VideoCapture(0)

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
