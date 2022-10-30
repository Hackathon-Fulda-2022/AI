import sounddevice
from scipy.io.wavfile import write

fs = 44100
second = 1


print(sounddevice.query_devices())
sounddevice.default.device = 1

for i in range(2):
    print("recorde")
    record_voice = sounddevice.rec( int( second * fs ) , samplerate = fs , channels = 1 )
    sounddevice.wait()
    write("out" + str(i) + ".wav", fs , record_voice )