import whisper
import sounddevice
import soundfile as sf
import numpy as np
import time


import DTHealth_AI_STT
import DTHealth_AudioDevice
import DTHealth_State_Macine

import Utils.interpreter
import Utils.translator

from API.api_lib import hackathon_api


if __name__ == "__main__":
    
    sttai = DTHealth_AI_STT.DTH_STT()
    audiodevice = DTHealth_AudioDevice.DTH_Audio_Device()
    audiodevice.setagree(".\\sound\\greeting\\")
    audiodevice.setgreeting(".\\sound\\agree\\")
    statemacine = DTHealth_State_Macine.DTHealth_StateMacine()

    audiodevice.start()
    sttai.setInitialVoiceDate(audiodevice.readBlock())

    api = hackathon_api()

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
                
                outkeys = Utils.interpreter.interpreter(result.text)
                vitals, medications, patientconditions, patientRequests = outkeys

                print(vitals)
                print(medications)
                print(patientconditions)
                print(patientRequests)

                audiodevice.sayText(result.text)

                # Send the evaluated dictionaries to the api
                #for vital in vitals:
                #    res = api.post_update_vitals(vital)
                #    if res != 200:
                #        print(f'API returned Error Code: {res}')
                #for medication in medications:
                #    res = api.post_update_medication(medication)
                #    if res != 200:
                #        print(f'API returned Error Code: {res}')
                #for patientcondition in patientconditions:
                #    res = api.post_update_patientcondition(patientcondition)
                #    if res != 200:
                #        print(f'API returned Error Code: {res}')
                #for patientRequest in patientRequests:
                #    res = api.post_new_patientRequest(patientRequest)
                #    if res != 200:
                #        print(f'API returned Error Code: {res}')

                





        


