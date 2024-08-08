import time
import os
import shutil
from pytube import YouTube, Playlist
from threading import Thread

MAX_THREADS = 4

def download_video(video_url, download_folder):
    try:
        yt = YouTube(video_url)
        print(f"Downloading: {yt.title}")
        yt.streams.first().download(download_folder)
        print("Download complete!")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")

def get_playlist_links(playlist_url):
    playlist = Playlist(playlist_url)
    return [video.watch_url for video in playlist.videos]

def create_download_folder(playlist_title):
    folder_name = playlist_title.replace(" ", "_")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def download_playlist(playlist_url, playlist_title):
    download_folder = create_download_folder(playlist_title)
    links = get_playlist_links(playlist_url)

    threads = []
    for link in links:
        thread = Thread(target=download_video, args=(link, download_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"All videos from '{playlist_title}' downloaded to '{download_folder}'")

if __name__name__ == "__main__":
    playlist_url = input("Enter playlist URL: ")
    playlist_title = input("Enter playlist title: ")
    download_playlist(playlist_url, playlist_title)
