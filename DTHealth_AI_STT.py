import numpy as np
import whisper
import numpy as np

class DTH_STT:
    def __init__(self, modelFraze :str = "medium", modelCommand : str = "large") -> None:
        print("Inizialize STT")
        self.modelFraze = whisper.load_model(modelFraze)
        self.modelCommand = whisper.load_model(modelCommand)
        self.voiceDataCommand = 0
        self.voice_data1 = 0
        self.voice_data2 = 0
    
    def do_infrence(self, voice_data)-> str:

        self.voice_data2 = voice_data

        audio = self.convertaudiosignal(np.append(self.voice_data1, self.voice_data2, axis=0))

        result = self.do_blocking_decode(audio, self.modelFraze, whisper.DecodingOptions())

        self.voice_data1 = self.voice_data2

        return result
    
    def Quarry_Cont_data(self, sound_Array: np.ndarray):
        self.voiceDataCommand = np.append(self.voiceDataCommand, sound_Array, axis=0)
    
    def Start_Quarry(self, sound_Array: np.ndarray):
        self.voiceDataCommand = sound_Array
    
    def Stop_Quarry(self) -> str:
        
        audio = self.convertaudiosignal(self.voiceDataCommand)

        result = self.do_blocking_decode(audio, self.modelCommand, whisper.DecodingOptions())

        return result

    def setInitialVoiceDate(self, array: np.ndarray):
        self.voiceDataCommand = array
        self.voice_data1 = array
        self.voice_data2 = array
    
    def convertaudiosignal(self, sound_Array : np.ndarray) -> np.ndarray:
        outAudio = np.squeeze(sound_Array)
        outAudio = whisper.pad_or_trim(outAudio)
        return outAudio

    def getlanguage(self, inp:str)->str:
        _, probs = inp
        return max(inp, key=inp.get)

    def do_blocking_decode(self, sound_Array: np.ndarray, model:whisper.model,options: whisper.DecodingOptions) -> str:
        
        mel = whisper.log_mel_spectrogram(sound_Array, n_mels=80).to(model.device)
        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)
        return result