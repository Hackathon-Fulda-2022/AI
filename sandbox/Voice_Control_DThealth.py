import whisper
import sounddevice
import soundfile as sf
from scipy.io.wavfile import write
import numpy as np
import time

def convertaudiosignal(sound_Array : np.ndarray) -> np.ndarray:
    outAudio = np.squeeze(sound_Array)
    outAudio = whisper.pad_or_trim(outAudio)
    return outAudio

def getlanguage(inp:str)->str:
    pass

def do_blocking_decode(sound_Array: np.ndarray, model:whisper.model,options: whisper.DecodingOptions) -> str:
    
    mel = whisper.log_mel_spectrogram(sound_Array, n_mels=80).to(model.device)
    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result

def is_start(message: str, catchfraze: str = ["anna", "hallo"])-> bool:
    message = message.lower()
    if all(x in message for x in catchfraze):
        return True
    else:
        return False

def is_stop(message: str, catchfraze: str = ["anna", "danke"])-> bool:
    message = message.lower()
    if all(x in message for x in catchfraze):
        return True
    else:
        return False

def is_fraze(message: str, catchfraze: str)-> bool:
    message = message.lower()
    if all(x in message for x in catchfraze):
        return True
    else:
        return False




if __name__ == "__main__":
    # Samples per second
    fs = 16000
    # MAX Record Seconds
    second = 4
    # Device
    device = 1

    #Standart texte
    stnadartJa, Jafs = sf.read("./Zustimmen_Gerne/ja.wav", dtype='float32')

    print("LoadModel")
    model_keyword = whisper.load_model("medium")
    model_listening = whisper.load_model("large")
    print("Model sucessfuly Loadet")


    print(sounddevice.query_devices())
    #sounddevice.default.device = [4, device] 
    print("Liadet Microfon: ", device)

    input_stream_keyword = sounddevice.InputStream(samplerate=fs, device=device, channels=1, blocksize=fs)

    input_stream_keyword.start()
    
    voice_data1 =  input_stream_keyword.read(fs)

    isinComandMode = False
    isinNormalMode = False

    print("Start Main Loop")
    while True:
        
        #print("Read")
        #Gather Data
        voice_data2 =  input_stream_keyword.read(fs)

        #getaudio signal
        audio = convertaudiosignal(np.append(voice_data1[0], voice_data2[0], axis=0))
        #record_voice = sounddevice.rec( int( second * fs ) , samplerate = fs , channels = 1 )
        result = do_blocking_decode(audio, model_keyword, whisper.DecodingOptions())
        voice_data1 = voice_data2

        #Speichert alles kontinuirlich gesprochene 
        if isinComandMode:
            voice_data_command = np.append(voice_data_command, voice_data2[0], axis=0)

        #Testet Keyword Debug 
        if is_start(result.text) or is_stop(result.text):
            
            print(result.text, "\nStart:", is_start(result.text), "Stop:", is_stop(result.text))
        
        #Testet Keyword Start Stop
        if isinComandMode == False and is_start(result.text):
            sounddevice.default.channels = 1
            sounddevice.playrec(stnadartJa, Jafs)
            voice_data_command = voice_data2[0]
            print("Stram Start")
            isinComandMode = True
        #Testet Keyword Start Stop
        if isinComandMode == True and is_stop(result.text):
            isinComandMode = False

            audiocommand = convertaudiosignal(voice_data_command)
            resultcommand = do_blocking_decode(audiocommand, model_listening, whisper.DecodingOptions())
            print(resultcommand.text)

        
