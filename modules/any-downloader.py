import yt_dlp

def download_x_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # Best quality available
        'outtmpl': output_path,               # Output file path
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    video_url = input("Paste link here: ")
    output_filename = input("Enter the output filename (e.g., foota_vid): ")
    # video_url = 'https://x.com/ahmednasirlaw/status/1851885906623353282?s=48'
    download_x_video(video_url, f'{output_filename}+.mp4')
