from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import whisper
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = whisper.load_model("base")

# Progress tracking
progress = {"status": "Idle"}


# Convert to VTT (browser supported)
def convert_to_vtt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")

        for seg in segments:
            start = seg['start']
            end = seg['end']
            text = seg['text']

            def format_time(t):
                hrs = int(t // 3600)
                mins = int((t % 3600) // 60)
                secs = int(t % 60)
                ms = int((t - int(t)) * 1000)
                return f"{hrs:02}:{mins:02}:{secs:02}.{ms:03}"

            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        progress["status"] = "Uploading video..."

        video = request.files["video"]
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        progress["status"] = "Extracting audio..."

        audio_path = os.path.join(UPLOAD_FOLDER, video.filename + ".wav")

        # 🔥 Strong FFmpeg extraction
        process = subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_path,
            "-y"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Debug FFmpeg output (optional)
        print(process.stderr.decode())

        # Check if audio exists
        if not os.path.exists(audio_path):
            progress["status"] = "Error: Audio file not created"
            return "Audio extraction failed"

        size = os.path.getsize(audio_path)
        print("Audio file size:", size)

        if size == 0:
            progress["status"] = "Error: Empty audio file"
            return "Audio extraction failed (empty file). Try another video."

        progress["status"] = "Generating captions..."

        try:
            result = model.transcribe(audio_path, fp16=False)
        except Exception as e:
            progress["status"] = "Error during transcription"
            return f"Transcription failed: {str(e)}"

        progress["status"] = "Finalizing subtitles..."

        vtt_path = os.path.join(OUTPUT_FOLDER, "subtitles.vtt")
        convert_to_vtt(result["segments"], vtt_path)

        progress["status"] = "Done"

        return render_template("index.html",
                               video=video.filename,
                               subtitles="subtitles.vtt")

    return render_template("index.html", video=None)


@app.route("/progress")
def get_progress():
    return jsonify(progress)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/static/outputs/<filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)