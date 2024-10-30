import voice_listener as listener
import transcriber as transcriber
import whisper_recorder as ws
import whisper

#Implement a pipeline for processing voices, get text, upsert to index db, fine-tune model, ouput results

def main():
    audio = ws.record_audio()
    txt = ws.transcribe_audio(audio, "base")
    print(txt)


if __name__ == "__main__":
    main()




