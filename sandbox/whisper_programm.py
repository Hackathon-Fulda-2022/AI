import whisper
import sounddevice
from scipy.io.wavfile import write
import numpy as np
import bessererAudioLoader

fs = 16000
second = 10
print("LoadModel")
model = whisper.load_model("medium")
print("Modelfinisched")




print(sounddevice.query_devices())
sounddevice.default.device = 1



for i in range(2):
    print("recorde")

    initialrecordrecord_voice = sounddevice.rec( int( second * fs ) , samplerate = fs , channels = 1 )
    
    #audio = whisper.load_audio("out0.wav")
    #audio2 = np.squeeze(record_voice)

    #print("Shape",audio.shape)
    #print("Shape",audio2.shape)
    #audio = whisper.pad_or_trim(audio)
    audio2 = np.squeeze(initialrecordrecord_voice)
    audioinKI = whisper.pad_or_trim(audio2)
    #print("Shape",audio.shape)
    print("Shape",audio2.shape)
    #rec = np.transpose(record_voice)
    mel = whisper.log_mel_spectrogram(audioinKI).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)



    # print the recognized text
    print(result.text)

