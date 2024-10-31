from google.cloud import texttospeech

def text_to_male_voice_audio(text, filename="output.mp3", language_code="en-US"):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set up the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters (e.g., language, gender)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Specify the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the output to a file
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to '{filename}'")

# Example usage
if __name__ == "__main__":
    text = "Hello, this is a male voice speaking!"
    text_to_male_voice_audio(text, filename="male_voice_output.mp3")
