import streamlit as st
from modules import voice_listener as listener
from modules import transcriber as transcriber
from modules import whisper_recorder as ws
import whisper
from modules import embedding as embed
import os
from modules import text_2_speech as tts

# Implement a pipeline for processing voices, getting text, upserting to index db, fine-tuning model, and outputting results
def main():
    st.title("Voice Processing and Transcription App")
    
    # Input for YouTube URL and model selection
    video_url = st.text_input("Enter YouTube video URL:")
    model_name = st.selectbox("Choose Whisper Model:", ["base", "small", "medium", "large"])
    
    if st.button("Start Transcription"):
        all_text = ""

        # Transcribe the YouTube video
        st.write("Transcribing YouTube video with Whisper...")
        yt_data = transcriber.transcribe_youtube_video(video_url, model_name)
        all_text += yt_data + "\n"  # Add YouTube transcription to all_text
        st.write("Transcription:")
        st.text(yt_data)

        # Save all collected text into a single file
        with open("outputs/transcription.txt", "w", encoding="utf-8") as file:
            file.write(all_text)
        # st.write("Transcription saved to outputs/transcription.txt")

        # Convert text to audio and save
        audio_path = "outputs/converted_audio.mp3"
        tts.text_to_audio(all_text, audio_path)
        st.audio(audio_path)

# Run the main function
if __name__ == "__main__":
    main()
