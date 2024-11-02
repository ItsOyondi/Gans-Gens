import os
import sys
import shutil
import subprocess
import yt_dlp
import tkinter as tk
from tkinter import messagebox
import requests
import zipfile
import tempfile

def check_ffmpeg():
    try:
        # Check if FFmpeg is installed
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def install_7zip():
    """Download and install 7-Zip if not already installed."""
    seven_zip_url = "https://www.7-zip.org/a/7z2408-x64.exe"  # Update to latest 7-Zip URL if necessary
    seven_zip_installer = "7z_setup.exe"

    try:
        # Download the 7-Zip installer
        response = requests.get(seven_zip_url, stream=True)
        response.raise_for_status()
        with open(seven_zip_installer, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Run the 7-Zip installer silently
        subprocess.run([seven_zip_installer, "/S"], check=True)

        # Remove the installer after installation
        os.remove(seven_zip_installer)
        
        return True
    except Exception as e:
        messagebox.showerror("Installation Error", f"Failed to install 7-Zip: {e}")
        return False

def install_ffmpeg():
    # Define FFmpeg download URL and paths
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z"
    ffmpeg_archive = "ffmpeg.7z"
    install_dir = r"C:\ffmpeg"  # Destination for FFmpeg installation

    try:
        # Download FFmpeg
        response = requests.get(ffmpeg_url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        with open(ffmpeg_archive, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Check if 7z is available, if not, install it
        if not shutil.which("7z"):
            if not install_7zip():
                return False  # Stop if 7-Zip installation fails

        # Extract the FFmpeg files using 7z command
        temp_dir = tempfile.mkdtemp()
        subprocess.run(["7z", "x", ffmpeg_archive, f"-o{temp_dir}"], check=True)

        # Move extracted files to the install directory
        shutil.move(temp_dir, install_dir)

        # Remove the downloaded archive and temporary directory
        os.remove(ffmpeg_archive)

        # Set the path to the FFmpeg bin folder
        ffmpeg_bin_path = os.path.join(install_dir, "bin")
        
        # Add the FFmpeg bin folder to PATH temporarily for this session
        current_path = os.environ.get("PATH", "")
        if ffmpeg_bin_path not in current_path:
            os.environ["PATH"] += os.pathsep + ffmpeg_bin_path
            
            # Optionally, add to the system PATH permanently
            # Requires admin rights
            import winreg as reg
            reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
            with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, current_path + os.pathsep + ffmpeg_bin_path)

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
