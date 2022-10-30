import whisper
import sounddevice
import soundfile as sf
import numpy as np
import time


import DTHealth_AI_STT
import DTHealth_AudioDevice
import DTHealth_State_Macine


if __name__ == "__main__":
    
    sttai = DTHealth_AI_STT.DTH_STT("medium", "medium")
    audiodevice = DTHealth_AudioDevice.DTH_Audio_Device()
    audiodevice.setagree(".\\Zustimmen_Gerne\\")
    audiodevice.setgreeting(".\\Standart_Gerne\\")
    statemacine = DTHealth_State_Macine.DTHealth_StateMacine()

    audiodevice.start()
    sttai.setInitialVoiceDate(audiodevice.readBlock())

    print("Start Main Loop")
    while True:
        
        audioblock = audiodevice.readBlock()

        result = sttai.do_infrence(audioblock)

        print(result.text)
        
        if statemacine.CommandState:
            sttai.Quarry_Cont_data(audioblock)

        if statemacine.eval_st_sp_state(result.text):

            if statemacine.CommandState:
                sttai.Start_Quarry(audioblock)
                audiodevice.sayGreetingFraze()
            if not statemacine.CommandState:
                result = sttai.Stop_Quarry()
                audiodevice.sayAgreeFraze()
                print(result.text)
        


