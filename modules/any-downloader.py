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

def install_py7zr():
    """Install py7zr if not already installed."""
    try:
        import py7zr
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
        import py7zr

def install_7zip():
    """Download and set up portable 7-Zip using py7zr if not already available."""
    install_py7zr()
    import py7zr
    
    seven_zip_url = "https://www.7-zip.org/a/7z2408-extra.7z"  # Portable version URL
    seven_zip_archive = "7z_portable.7z"
    temp_dir = tempfile.mkdtemp()
    seven_zip_dir = os.path.join(temp_dir, "7zip")

    try:
        # Download the portable 7-Zip archive
        response = requests.get(seven_zip_url, stream=True)
        response.raise_for_status()
        with open(seven_zip_archive, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract the 7-Zip files using py7zr
        with py7zr.SevenZipFile(seven_zip_archive, mode='r') as archive:
            archive.extractall(path=seven_zip_dir)

        # Remove the downloaded archive after extraction
        os.remove(seven_zip_archive)
        
        # Return the path to the portable 7-Zip executable (7za.exe)
        return os.path.join(seven_zip_dir, "7za.exe")
    except Exception as e:
        messagebox.showerror("Installation Error", f"Failed to set up 7-Zip: {e}")
        return None

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

        # Check if 7za is available, if not, download and set up portable 7-Zip
        seven_zip_exe = shutil.which("7za") or install_7zip()
        if not seven_zip_exe:
            return False  # Stop if 7-Zip setup fails

        # Extract the FFmpeg files using 7za command
        temp_dir = tempfile.mkdtemp()
        subprocess.run([seven_zip_exe, "x", ffmpeg_archive, f"-o{temp_dir}"], check=True)

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
