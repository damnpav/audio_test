import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()


device_index = None
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"i = {i}; dev_name is {dev['name']}; host_api is {dev['hostApi']}")
    if "Агрегат" in dev['name']:  # Replace with the actual name of your Aggregate Device
        device_index = i
        break
print(f'chosen device index is {i}')
#device_index = 2
# Ensure the virtual device was found
if device_index is None:
    raise Exception("Could not find BlackHole/Soundflower virtual audio device.")

# Open stream
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("Recording...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
