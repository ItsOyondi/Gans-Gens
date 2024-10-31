
import pyttsx3 

def ptts_text_audio(text):
    # Initialize the converter 
    converter = pyttsx3.init() 
    voices = converter.getProperty('voices') 
    
    for voice in voices: 
        print("Voice:") 
        print("ID: %s" %voice.id) 
        print("Name: %s" %voice.name) 
        print("Age: %s" %voice.age) 
        print("Gender: %s" %voice.gender) 
        print("Languages Known: %s" %voice.languages) 
    
    # Sets speed percent  
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    converter.setProperty('rate', 150)
    converter.setProperty('voice', voice_id) 
    # Set volume 0-1 
    converter.setProperty('volume', 0.7) 
    converter.say(text) 
    # Empties the say() queue 
    converter.runAndWait()

if __name__ == "__main__":
    text = "Hi, i am just a robot. I was created by oyos. Kuwa na siku njema."
    ptts_text_audio(text)