import pyaudio
import wave

# Set the parameters for the recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sample rate
CHUNK = 1024              # Frames per buffer
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream for recording
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index=1,
                frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Start recording
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
