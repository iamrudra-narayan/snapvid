# app.py
import re
import os
from flask import Flask, render_template, request, redirect
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        # Sanitize the video title and limit its length to 100 characters
        title = sanitize_filename(yt.title)[:100]

        # Adjust the download path to the 'downloads' folder
        download_path = os.path.join("downloads", f"{title}.mp4")
        stream.download(output_path="downloads", filename=title)

        return redirect('/')
    except Exception as e:
        return f"Error: {e}"

def sanitize_filename(filename):
    # Remove characters that are not allowed in filenames
    # For example, on Windows, characters like '\', '/', ':', '*', '?', '"', '<', '>', '|'
    return re.sub(r'[\\/:*?"<>|]', '', filename)

if __name__ == '__main__':
    # Create the 'downloads' folder if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    app.run(debug=True)
