from __future__ import unicode_literals
import yt_dlp as youtube_dl
import whisper


def transcribe_youtube_video(video_url, ws_model):

    # Define the download options
    ydl_opts = {
        'format': 'bestaudio/best',  
        'outtmpl': 'audio.%(ext)s',  
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Load the Whisper model
    model = whisper.load_model(ws_model)  # Use "base" or "small" for faster performance, or "large" for accuracy
    transcription = model.transcribe("audio.mp3") 

    # Save the transcription to a text file
    with open("transcription.txt", "w", encoding="utf-8") as file:
        file.write(transcription["text"])

    print("Transcription completed and saved to transcription.txt")

if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=YkATEgnX51k'
    transcribe_youtube_video(video_url, "base")

