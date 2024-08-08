import time
import os
from pytube import YouTube

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        print(f"Downloading: {yt.title}")
        yt.streams.first().download()
        print("Download complete!")
    except Exception as e:
        print(f"Error: {e}")

video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
download_video(video_url)
