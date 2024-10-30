import whisper
import soundfile as sf
import pyaudio
import wave

# Configuration for recording
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono channel
RATE = 16000  # Sample rate for Whisper compatibility
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 5  # Duration of recording
OUTPUT_FILENAME = "recorded_audio.wav"

# Function to record audio
def record_audio():
    audio = pyaudio.PyAudio()
    
    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recorded audio to a .wav file
    with wave.open(OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return OUTPUT_FILENAME


# Step 3: Transcribe audio using Whisper
def transcribe_audio(audio_file, model):
    model = whisper.load_model(model)
    result = model.transcribe(audio_file)
    print("Audio Transcription completed...")

    return result["text"]


# Run the recording and transcription
# audio_file = record_audio()
# transcribe_audio(audio_file)
