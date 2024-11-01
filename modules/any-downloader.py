import os
import sys
import subprocess
import yt_dlp
import tkinter as tk
from tkinter import messagebox

def check_ffmpeg():
    try:
        # Check if FFmpeg is installed
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def install_ffmpeg():
    # Download and install FFmpeg for Windows
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    ffmpeg_zip = "ffmpeg.7z"
    
    try:
        # Download FFmpeg
        import requests
        response = requests.get(ffmpeg_url)
        with open(ffmpeg_zip, "wb") as f:
            f.write(response.content)

        # Extract the FFmpeg files (requires py7zr)
        import py7zr
        with py7zr.SevenZipFile(ffmpeg_zip, mode='r') as z:
            z.extractall("ffmpeg")

        # Clean up the downloaded zip file
        os.remove(ffmpeg_zip)

        # Set the path to the extracted ffmpeg folder
        ffmpeg_extracted_path = os.path.join(os.getcwd(), "ffmpeg", "bin")

        # Add the FFmpeg bin folder to PATH temporarily for this session
        os.environ["PATH"] += os.pathsep + ffmpeg_extracted_path

        return True
    except Exception as e:
        messagebox.showerror("Installation Error", f"Failed to install FFmpeg: {e}")
        return False

def download_x_video(url, output_path):
    # Use the updated path to FFmpeg
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def start_download():
    video_url = url_entry.get()
    output_filename = filename_entry.get()

    if not video_url or not output_filename:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    output_path = f'{output_filename}.mp4'

    try:
        if not check_ffmpeg():
            if not install_ffmpeg():
                return

        download_x_video(video_url, output_path)
        messagebox.showinfo("Success", f"Downloaded: {output_path}")
        root.quit()
    except Exception as e:
        messagebox.showerror("Download Error", str(e))
        root.quit()

# Create the main window
root = tk.Tk()
root.title("Video Downloader")

# Create and place the URL label and entry
url_label = tk.Label(root, text="Paste video URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the filename label and entry
filename_label = tk.Label(root, text="Enter output filename (without extension):")
filename_label.pack(pady=5)

filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# Create and place the download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

# Run the application
root.mainloop()
