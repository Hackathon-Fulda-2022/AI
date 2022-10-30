import whisper
import sounddevice
from scipy.io.wavfile import write
import numpy as np
import time


def callback(indata, frame_count, time_info, status):
    print(indata.shape)
    print(frame_count)
    print(time_info)
    print(status)


if __name__ == "__main__":
    # Samples per second
    fs = 16000
    # MAX Record Seconds
    second = 4
    # Device
    device = 1

    print(sounddevice.query_devices())
    sounddevice.default.device = device
    print("Liadet Microfon: ", device)

    #record_voice = sounddevice.rec( int( second * fs ) , samplerate = fs , channels = 1 )
    #recstream = sounddevice.get_stream()
    input_stream = sounddevice.InputStream(samplerate=fs, device=device,
                                            channels=1, callback=callback, blocksize=16000)
    input_stream.start()
    for i in range(100000):
        time.sleep(0.2)
        print("Time")

        #print(record_voice.shape)