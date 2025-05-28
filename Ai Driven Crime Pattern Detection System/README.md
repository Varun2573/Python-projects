# 🛡️ AI Driven Crime Pattern Detection System : Home Safety

This project is a full-stack solution for detecting crimes from CCTV footage (uploaded or real-time), storing flagged videos in MongoDB using GridFS, and providing an authenticated user portal to stream video evidence. Built using FastAPI, PostgreSQL for user authentication, MongoDB for evidence storage, and Jinja2 templates for the frontend.

---

## 📌 Features

- 🔐 **User Authentication** (Login system via PostgreSQL)
- 📹 **Video Upload and Real-Time Camera Capture**
- 🧠 **AI-Powered Crime Detection** via Gemini API
- 💾 **Video Storage in MongoDB (GridFS)**
- 🎥 **Video Streaming Interface for Users**
- 🔔 **Twilio SMS Alerts on Crime Detection**
- 🌐 **Simple Web UI with Jinja2 Templates**

---

## 📦 Technologies Used

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Backend framework |
| **Jinja2**  | HTML templating |
| **MongoDB + GridFS** | Video storage and streaming |
| **PostgreSQL** | User authentication |
| **OpenCV** | Frame extraction from video |
| **Google Gemini API** | Crime classification |
| **Twilio API** | Alerting mechanism |

---

## 🛠️ Requirements

- Python 3.8+
- PostgreSQL server
- MongoDB server
- pgAdmin (optional, for DB admin)
- Google Gemini API key
- Twilio Account (for SMS)

### Python Dependencies

---bash
fastapi
uvicorn
pymongo
python-dotenv
jinja2
psycopg2-binary
opencv-python
twilio


---

## Setup .env file

DB_URL=postgresql://username:password@localhost:5432/yourdb
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_token
TWILIO_FROM=your_twilio_number
TWILIO_TO=recipient_number
GEMINI_API_KEY=your_gemini_api_key

## Create a table in PostgreSQL to register the user

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


## Run the Application

- We have two portals. One is Detection Portal and another is User Portal.
- Detection portal will have video uplods and real time capture options where the detction will happen based on the option.
- If the video contains any crime the user is notified with an SMS alert using TWILIO.
- And evidence video is been stored into MOngoDb.
- User portal will have the login feature where the registered user will be given access.
- Then user can login ad check for evidence.

## Commands

- uvicorn "Detection Portal:app" --reload  (http://127.0.0.1:8000)

- uvicorn "User Portal:app" --host 0.0.0.0 --port 8001 --reload (http://127.0.0.1:8001)