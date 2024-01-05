import pyaudio
import whisper
import wave
from datetime import datetime as dt
from db_fun import initialize_cursor, check_for_order, audio_completed, record_audio_file


# Set the parameters for the recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sample rate
CHUNK = 1024              # Frames per buffer
# RECORD_SECONDS = 15        # Duration of recording
WAVE_OUTPUT_FILENAME = "audio_files/"
SECONDS_PERIOD = 30
num_frames_to_keep = int((RATE / CHUNK) * SECONDS_PERIOD)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Print available channels
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"i = {i}; dev_name is {dev['name']}; host_api is {dev['hostApi']}")
    print(f"Max Input Channels = {dev['maxInputChannels']}; Max Output Channels = {dev['maxOutputChannels']}\n")

# TODO select static devices
input_device = int(input('\nWrite your input device\n'))
CHANNELS = int(input('\nWrite numbers of channels\n'))

cursor, conn = initialize_cursor()

print("Recording...")
stop = 0

while stop == 0:
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, input_device_index=input_device,
                    frames_per_buffer=CHUNK)
    frames = []
    flag = 0

    while flag == 0:
        try:
            data = stream.read(CHUNK)
            frames.append(data)

            if len(frames) > num_frames_to_keep:
                frames.pop(0)

            if check_for_order(conn):
                flag = 1
                stop = 1
        except Exception as e:
            print(f'Exception at recording: {e}')
            flag = 1
            stop = 1

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio_completed(cursor, conn)
    audio_file_path = WAVE_OUTPUT_FILENAME + f"output_{dt.now().strftime('%H_%M_%S_%d_%m')}.wav"
    wf = wave.open(audio_file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    record_audio_file(audio_file_path, cursor, conn)



