import os
import cv2
import time
import base64
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

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
        if frame_count % int(fps * frame_interval) == 0:  # Extract every 5 seconds
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

# Function to detect crime in the video
def detect_crime_in_video(video_path):
    frames_folder = "frames"
    print("Extracting key frames from video...")
    key_frames = extract_key_frames(video_path, frames_folder)

    if not key_frames:
        return "No frames extracted. Check the video file."

    print(f"Extracted {len(key_frames)} frames. Sending to Gemini API...")

    model = genai.GenerativeModel("gemini-1.5-pro")  # Use "gemini-1.5-flash" for faster results
    images_data = encode_images(key_frames)

    prompt_text = """
    Analyze these images and determine the overall crime type occurring in the video.
    Possible crimes include theft, robbery, assault, vandalism, or suspicious behavior.
    If no crime is visible, then display no crime detected.
    """

    try:
        response = model.generate_content([
            {"role": "user", "parts": images_data + [{"text": prompt_text}]}
        ])

        return response.text if response else "No response from API."

    except Exception as e:
        return f"Error processing video: {str(e)}"

# Example usage
video_path = "testing.webm"
crime_report = detect_crime_in_video(video_path)
print("\nFinal Crime Report:\n", crime_report)
