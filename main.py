import time
import os
from pytube import YouTube, Playlist

def download_video(video_url, download_folder):
    try:
        yt = YouTube(video_url)
        print(f"Downloading: {yt.title}")
        yt.streams.first().download(download_folder)
        print("Download complete!")
    except Exception as e:
        print(f"Error: {e}")

def get_playlist_links(playlist_url):
    playlist = Playlist(playlist_url)
    links = []
    for video in playlist.videos:
        links.append(video.watch_url)
    return links

def create_download_folder(playlist_title):
    folder_name = playlist_title.replace(" ", "_")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# Testing playlist download
playlist_url = input("Enter playlist URL: ")
playlist_title = input("Enter playlist title: ")
links = get_playlist_links(playlist_url)

download_folder = create_download_folder(playlist_title)

for link in links:
    download_video(link, download_folder)
