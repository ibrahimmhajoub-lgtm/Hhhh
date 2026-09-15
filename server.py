from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/formats", methods=["POST"])
def get_formats():
    url = request.json["url"]
    result = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True)
    return jsonify({"formats": result.stdout})

@app.route("/download", methods=["POST"])
def download_video():
    url = request.json["url"]
    fmt = request.json["format"]
    output_file = "video.%(ext)s"
    subprocess.run(["yt-dlp", "-f", fmt, url, "-o", output_file])
    for ext in ["mp4", "mkv", "webm"]:
        if os.path.exists(f"video.{ext}"):
            return send_file(f"video.{ext}", as_attachment=True)
    return jsonify({"error": "لم يتم العثور على الملف"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
