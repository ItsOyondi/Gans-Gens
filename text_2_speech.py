from gtts import gTTS
import os

def text_to_audio(text, filename, language="en"):
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Save the converted audio in an mp3 file
    tts.save(filename)
    print(f"Audio saved as {filename}")
    # Optionally, play the audio file (works on many systems)
    os.system(f"start {filename}")

# Example usage
if __name__ == "__main__":
    text = "Hi, i am just a robot. I was created by oyos. Kuwa na siku njema."
    text_to_audio(text, filename="hello.mp3", language="en")
