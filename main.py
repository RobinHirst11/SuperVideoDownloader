import time
import os
import shutil
from pytube import YouTube, Playlist

BASE_DOWNLOAD_LOCATION = "downloaded_videos"

def main():
    """Main loop for the video downloader application."""
    print_header()
    while True:
        print_options()
        choice = input("\nYour choice: ")
        execute_choice(choice)

def print_header():
    """Prints a stylish header for the application."""
    print("\033[1;36;40m**********************************************")
    print("      Welcome to SuperVideo Downloader!")
    print("**********************************************\033[m")

def print_options():
    """Prints available options for the user."""
    print("\nChoose an option:")
    print("\033[1;32m1. Get video links")
    print("2. Download videos")
    print("3. Delete videos")
    print("0. Exit\033[m")

def execute_choice(choice):
    """Executes user's choice."""
    if choice == '1':
        get_links()
    elif choice == '2':
        download_videos()
    elif choice == '3':
        delete_videos()
    elif choice == '0':
        exit_program()
    else:
        print("\033[1;31mInvalid choice. Please try again.\033[m")

def get_links():
    """Extracts video links from a YouTube playlist and saves them to files."""
    print("\n\033[1;36mGET VIDEO LINKS\033[m")
    playlist_link = input("\nEnter the YouTube playlist URL: ")
    base_filename = input("Enter a base filename for the links (e.g., my_playlist): ")
    folder_name = input("Enter the folder name to store text files: ")

    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    write_playlist_to_files(playlist_link, base_filename, folder_path)
    print(f"\033[1;32mPlaylist links saved to '{folder_name}' folder.\033[m")

def write_playlist_to_files(playlist_url, base_filename, folder_path):
    """Splits playlist links into multiple text files for efficient handling."""
    playlist = Playlist(playlist_url)
    file_index = 1

    with open(os.path.join(folder_path, f"{base_filename}_{file_index}.txt"), 'w') as current_file:
        for index, video_url in enumerate(playlist.video_urls):
            current_file.write(f"{video_url}\n")
            if (index + 1) % 20 == 0:
                current_file.close()
                file_index += 1
                current_file = open(os.path.join(folder_path, f"{base_filename}_{file_index}.txt"), 'w')

def download_videos():
    """Downloads videos from text files of links."""
    print("\n\033[1;36mDOWNLOAD VIDEOS\033[m")
    folder_list = get_folder_list()
    if not folder_list:
        print("\033[1;31mNo folders found in the specified directory.\033[m")
        return

    print("\nChoose a folder containing text files:")
    for index, folder_name in enumerate(folder_list):
        print(f"{index}: {folder_name}")

    choice = input("\nEnter the folder number: ")

    try:
        choice = int(choice)
        if 0 <= choice < len(folder_list):
            folder_path = os.path.join(os.getcwd(), folder_list[choice])
            download_videos_from_folder(folder_path)
        else:
            print("\033[1;31mInvalid choice. Please enter a valid folder number.\033[m")
    except ValueError:
        print("\033[1;31mInvalid input. Please enter a number.\033[m")

def get_folder_list():
    """Get the list of folders in the current directory."""
    folder_list = []
    for folder_name in os.listdir(os.getcwd()):
        if os.path.isdir(folder_name) and not folder_name.startswith('.') and folder_name != BASE_DOWNLOAD_LOCATION:
            folder_list.append(folder_name)
    return folder_list

def download_videos_from_folder(folder_path):
    """Downloads videos from text files within the specified folder."""
    file_list = get_file_list(folder_path)
    if not file_list:
        print("\033[1;31mNo text files found in the specified folder.\033[m")
        return

    print("\nChoose a text file to download videos from:")
    for index, file_name in enumerate(file_list):
        print(f"{index}: {file_name}")

    choice = input("\nEnter the file number: ")

    try:
        choice = int(choice)
        if 0 <= choice < len(file_list):
            file_path = os.path.join(folder_path, file_list[choice])
            download_videos_from_file(file_path)
        else:
            print("\033[1;31mInvalid choice. Please enter a valid file number.\033[m")
    except ValueError:
        print("\033[1;31mInvalid input. Please enter a number.\033[m")

def get_file_list(folder_path):
    """Get the list of text files in the specified folder."""
    file_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_list.append(file_name)
    return file_list

def create_download_folder():
    """Creates a download folder with a timestamp."""
    download_folder = os.path.join(BASE_DOWNLOAD_LOCATION, str(int(time.time())))
    os.makedirs(download_folder)
    return download_folder

def download_videos_from_file(file_path):
    """Downloads videos from the specified text file."""
    with open(file_path, 'r') as file:
        links = file.readlines()

    folder_name = os.path.splitext(os.path.basename(file_path))[0]
    download_folder = os.path.join(BASE_DOWNLOAD_LOCATION, folder_name)

    for index, link in enumerate(links):
        download_video(link.strip(), download_folder, index + 1, len(links))

def download_video(video_url, download_path, video_index, total_videos):
    """Downloads a single video and displays progress."""
    try:
        video = YouTube(video_url, on_progress_callback=on_progress)
        print(f"\n({video_index}/{total_videos}) \033[1;34mDownloading: {video.title}\033[m")
        video.streams.first().download(download_path)
        print("\033[1;32mDownload complete!\033[m")
    except Exception as e:
        print(f"\033[1;31mError downloading video ({video_url}): {e}\033[m")

def on_progress(stream, chunk, bytes_remaining):
    """Displays a simple download progress bar."""
    progress_percent = int(100 - (bytes_remaining / stream.filesize * 100))
    progress_bar = '█' * (progress_percent // 5) + '░' * (20 - progress_percent // 5)
    print(f"\r{progress_bar} {progress_percent}%", end='')

def delete_videos():
    """Deletes a folder of downloaded videos."""
    print("\n\033[1;36mDELETE VIDEOS\033[m")
    folder_name = input("\nEnter the name of the folder to delete: ")
    folder_path = os.path.join(BASE_DOWNLOAD_LOCATION, folder_name)

    if not os.path.exists(folder_path):
        print(f"\033[1;31mFolder '{folder_name}' does not exist.\033[m")
        return

    confirmation = input(f"\033[1;31mWARNING: Are you sure you want to delete ALL contents of '{folder_name}'? [y/n] \033[m")
    if confirmation.lower() != 'y':
        print("\033[1;32mDeletion canceled.\033[m")
        return

    try:
        shutil.rmtree(folder_path)
        print(f"\033[1;32mFolder '{folder_name}' and its contents deleted successfully.\033[m")
    except OSError as e:
        print(f"\033[1;31mError deleting folder: {e}\033[m")

def exit_program():
    """Exits the program."""
    print("\n\033[1;36mThank you for using SuperVideo Downloader! Goodbye.\033[m")
    exit()

if __name__ == "__main__":
    main()
