import threading
from flask import Flask, render_template, request, send_file
from pytube import YouTube
import re
import os
import schedule
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
            video_url = request.form.get('video_url')
            new_directory = 'downloads'
            os.makedirs(new_directory, exist_ok=True)

            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()

            # Clean up the video title using regex
            cleaned_title = re.sub(r'[^\w\s-]', '', yt.title)
            cleaned_title = re.sub(r'\s+', '-', cleaned_title)

            filename = cleaned_title + '.mp4'
            video_stream.download(output_path=new_directory, filename=filename)

            # Send the file as an attachment
            response = send_file(os.path.join(new_directory, filename), as_attachment=True)

            # Schedule the deletion of the downloaded video after 10 minutes
            schedule.every(10).minutes.do(delete_video, filename)

            return response
    return render_template('videoDownloader.html')

def delete_video(filename):
    downloads_dir = 'downloads'
    file_path = os.path.join(downloads_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted {filename}")
    else:
        pass

def schedule_cleanup():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/PrivacyPolicy')
def privacy():
    return render_template('privacy.html')        

if __name__ == '__main__':
    app.run(debug=False)
    schedule_thread = threading.Thread(target=schedule_cleanup)
    schedule_thread.start()
