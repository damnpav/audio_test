import pyaudio
import wave
from datetime import datetime as dt
import time
from db_fun import initialize_cursor, check_for_order, audio_completed, record_audio_file, stop_check


# Set the parameters for the recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
RATE = 44100              # Sample rate
CHUNK = 1024              # Frames per buffer
WAVE_OUTPUT_FILENAME = "/Users/dp_user/PycharmProjects/audio_test/release/audio_files/"
SECONDS_PERIOD = 30
num_frames_to_keep = int((RATE / CHUNK) * SECONDS_PERIOD)

input_device = 7
CHANNELS = 2

p = pyaudio.PyAudio()
cursor, conn = initialize_cursor()
stop = 0

def handle_audio_stream():
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=input_device,
                        frames_per_buffer=CHUNK)
        frames = []
        while True:
            if stop_check(conn):
                break
            data = stream.read(CHUNK)
            frames.append(data)
            if len(frames) > num_frames_to_keep:
                frames.pop(0)
            if check_for_order(conn):
                stream.stop_stream()
                stream.close()
                break
    except Exception as e:
        print(f'Exception at recording: {e}')
        return False, None  # Indicate an error and return no frames
    finally:
        stream.stop_stream()
        stream.close()
    return True, frames  # Indicate success and return the recorded frames


while not stop:
    success, recorded_frames = handle_audio_stream()
    if success and recorded_frames:
        # Save the recorded frames to a file
        audio_completed(cursor, conn)
        audio_file_path = WAVE_OUTPUT_FILENAME + f"output_{dt.now().strftime('%H_%M_%S_%d_%m')}.wav"
        wf = wave.open(audio_file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(recorded_frames))
        wf.close()
        record_audio_file(audio_file_path, cursor, conn)
    elif not success:
        print("Reinitializing stream...")
        time.sleep(1)  # Optional: wait before reinitializing



