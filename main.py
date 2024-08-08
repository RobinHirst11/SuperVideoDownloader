import time
import os
from pytube import YouTube, Playlist

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        print(f"Downloading: {yt.title}")
        yt.streams.first().download()
        print("Download complete!")
    except Exception as e:
        print(f"Error: {e}")

def get_playlist_links(playlist_url):
    playlist = Playlist(playlist_url)
    links = []
    for video in playlist.videos:
        links.append(video.watch_url)
    return links

playlist_url = "https://www.youtube.com/playlist?list=PLwL0y982280j_t222t222t222t222t222"
links = get_playlist_links(playlist_url)

for link in links:
    download_video(link)
