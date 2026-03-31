## AI Caption Generator

An AI-powered web app that generates captions for uploaded videos using OpenAI Whisper.

## Features

* Upload any video file
* Automatically generate captions
* Display subtitles on video
* Download subtitles (.vtt file)
* Clean and simple UI

## Tech Stack

* Python
* Flask
* OpenAI Whisper
* FFmpeg
* HTML, CSS, JavaScript

## Installation & Setup

### 🔹 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-caption-generator.git
cd ai-caption-generator

```
### 🔹 2. Install Python (if not installed)

Download from: https://www.python.org/downloads/

✔ Make sure to check **"Add Python to PATH"** during installation

### 🔹 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 🔹 4. Install FFmpeg

#### Windows:

1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/
2. Extract the ZIP file
3. Add the `bin` folder to System PATH

#### Verify installation:

```bash
ffmpeg -version
```

## ▶️ Running the Application

```bash
python app.py
```
Then open your browser and go to:

```
http://127.0.0.1:5000
```
## 📁 Project Structure

```
ai-caption-generator/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── outputs/
│
├── uploads/
```

## 👩‍💻 Author

**Shreya Jain**


