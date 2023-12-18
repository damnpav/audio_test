import pyaudio
import whisper
import wave
from datetime import datetime as dt
from db_fun import initialize_cursor, check_for_order


# Set the parameters for the recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sample rate
CHUNK = 1024              # Frames per buffer
# RECORD_SECONDS = 15        # Duration of recording
WAVE_OUTPUT_FILENAME = "audio_files/"
SECONDS_PERIOD = 30

# Initialize PyAudio
p = pyaudio.PyAudio()


# Print available channels
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"i = {i}; dev_name is {dev['name']}; host_api is {dev['hostApi']}")

cursor, conn = initialize_cursor()

print("Recording...")
stop = 0

while stop == 0:
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, input_device_index=1,
                    frames_per_buffer=CHUNK)
    frames = []
    flag = 0

    while flag == 0:
        data = stream.read(CHUNK)
        frames.append(data)

        if check_for_order():
            flag = 1

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME + f"output_{dt.now().strftime('%H_%M_%S_%d_%m')}.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


