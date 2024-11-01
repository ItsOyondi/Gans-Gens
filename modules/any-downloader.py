import yt_dlp
import tkinter as tk
from tkinter import messagebox

def download_x_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Best quality available
        'outtmpl': output_path,                # Output file path
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
        download_x_video(video_url, output_path)
        messagebox.showinfo("Success", f"Downloaded: {output_path}")
        root.quit()  # Exit after success
    except Exception as e:
        messagebox.showerror("Download Error", str(e))
        root.quit()  # Exit after error

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
