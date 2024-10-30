import voice_listener as listener
import transcriber as transcriber
import whisper_recorder as ws
import whisper
import embedding as embed
import os

#Implement a pipeline for processing voices, get text, upsert to index db, fine-tune model, ouput results
def main(model_name, video_url, embed_model, index_path):
    all_text = ""
    ############################ With Whisper #####################################
    print("Now recording on whisper ...\n\n")
    audio = ws.record_audio()
    txt = ws.transcribe_audio(audio, model_name)
    all_text += txt + "\n"  # Add Whisper transcription to all_text
    print(txt, "\n")

    ########################### Google Speech Recognition ########################
    print("Now recording... on Google Speech Recognition ...\n\n")
    audio_file_path = listener.record_audio()
    gg_txt = listener.get_recorded(audio_file_path)
    all_text += gg_txt + "\n"  # Add Google transcription to all_text
    print(gg_txt, "\n")

    ################################ Youtube Transcriber #########################
    print("Transcribing Youtube video with whisper ... \n\n")
    yt_data = transcriber.transcribe_youtube_video(video_url, model_name)
    all_text += yt_data + "\n"  # Add YouTube transcription to all_text
    print(yt_data, "\n")

    # Save all collected text into a single file
    with open("transcription.txt", "w", encoding="utf-8") as file:
        file.write(all_text)

    #The text saved will be used for embedding and building RAG in gpt model


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=KtYJX6phYFQ'
    model_name = "base"
    main(model_name, video_url)




