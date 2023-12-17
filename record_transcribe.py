import pyaudio
import whisper
import numpy as np
import wave
from datetime import datetime as dt

model = whisper.load_model('base')


# Set the parameters for the recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sample rate
CHUNK = 1024              # Frames per buffer
RECORD_SECONDS = 15        # Duration of recording
WAVE_OUTPUT_FILENAME = "output.wav"


# Initialize PyAudio
p = pyaudio.PyAudio()


# Print available channels
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"i = {i}; dev_name is {dev['name']}; host_api is {dev['hostApi']}")


stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index=1,
                frames_per_buffer=CHUNK)
print("Recording...")

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream_closing_start = dt.now()
# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()
stream_closing_end = dt.now()

wave_saving_start = dt.now()
# Save the recorded data as a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
wave_saving_end = dt.now()

model_start = dt.now()
result = model.transcribe(audio=WAVE_OUTPUT_FILENAME)
print(result['text'])
model_end = dt.now()

print(f'Timing:\n')
print(f'Stream closing time: {(stream_closing_end - stream_closing_start).seconds}')
print(f'Wave saving time: {(wave_saving_end - wave_saving_start).seconds}')
print(f'Model run time: {(model_end - model_start).seconds}')
