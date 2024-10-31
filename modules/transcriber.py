from __future__ import unicode_literals
import yt_dlp as youtube_dl
import whisper
import os

def transcribe_youtube_video(video_url, ws_model):
    # Ensure the outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # Define the download options
    ydl_opts = {
        'format': 'bestaudio/best',  
        'outtmpl': 'outputs/audio.%(ext)s',  # Save audio to outputs folder
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Load the Whisper model
    model = whisper.load_model(ws_model) 
    options = whisper.DecodingOptions(fp16=False)

    # Transcribe audio
    transcription = model.transcribe("outputs/audio.mp3", task="translate", language='en') 

    print("Transcription completed and saved to transcription.txt")
    return transcription["text"]



# if __name__ == "__main__":
#     video_url = 'https://www.youtube.com/watch?v=YkATEgnX51k'
#     transcribe_youtube_video(video_url, "medium")

