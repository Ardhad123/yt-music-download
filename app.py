import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
from PIL import Image
import urllib.parse

app = Flask(__name__)
CORS(app) 
DOWNLOAD_FOLDER = 'downloads'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def crop_to_square(image_path):
    img = Image.open(image_path)
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    img_cropped = img.crop((left, top, right, bottom))
    square_path = os.path.splitext(image_path)[0] + "_1x1.jpg"
    img_cropped.convert('RGB').save(square_path, "JPEG")
    return square_path

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'm4a/bestaudio/best', 
        'extractor_args': {'youtube': ['player_client=android,ios']},
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'cookiefile': 'cookies.txt',  # <--- COOKIES WAPAS LAGA DI HAIN
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'}
        ],
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            base_filename = ydl.prepare_filename(info_dict)
            base_name_no_ext = os.path.splitext(base_filename)[0]
            
            mp3_path = base_name_no_ext + '.mp3'
            original_thumb_path = base_name_no_ext + '.jpg'
            
            # Crop to square
            square_thumb_path = crop_to_square(original_thumb_path)
            
            mp3_filename = urllib.parse.quote(os.path.basename(mp3_path))
            img_filename = urllib.parse.quote(os.path.basename(square_thumb_path))

            return jsonify({
                "success": True,
                "mp3_file": mp3_filename,
                "img_file": img_filename
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_file/<filename>')
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, urllib.parse.unquote(filename))
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
