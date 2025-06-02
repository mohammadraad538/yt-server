from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    format_id = data.get("format", "bestaudio/best")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "format": format_id,
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "extract_flat": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return jsonify(info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "yt-dlp server is running!"

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
