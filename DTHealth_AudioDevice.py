from cgi import test
from os import listdir
from os.path import isfile, join
import sounddevice
import soundfile as sf
import numpy as np
import random

import sys
from urllib import response
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
from tempfile import gettempdir
import time





class DTH_Audio_Device:
    def __init__(self, inpdev=1, samplerate = 16000, maxintervalsec = 4, inputoutputdevice = None):
        print("Audiodevice Inizalisation")
        self.sf = samplerate
        self.maxsec = maxintervalsec
        self.iodevices = inputoutputdevice
        self.ageefrazes = []
        self.greetingfrazes = []
        self.standart = 0
        self.polly = boto3.client('polly')
        print(sounddevice.query_devices())
        #sounddevice.default.device = (inpdev, 13)
        sounddevice.default.channels = 1
        #Input Stream
        self.input_stream_keyword = sounddevice.InputStream(samplerate=self.sf, device=inpdev, channels=1, blocksize=self.sf)
    
    def sayAgreeFraze(self):
        sounddevice.playrec(random.choice(self.ageefrazes), self.standart)
        status = sounddevice.wait() 
    def sayGreetingFraze(self):
        sounddevice.playrec(random.choice(self.greetingfrazes), self.standart)
        status = sounddevice.wait() 

    def start(self):
        self.input_stream_keyword.start()

    def stop(self):
        self.input_stream_keyword.stop()

    def readBlock(self) -> np.ndarray:
        return self.input_stream_keyword.read(self.sf)[0]

    def setagree(self, folder: str):
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        print(onlyfiles)
        self.ageefrazes.clear()
        for i in onlyfiles:
            arrelem, self.standart = sf.read(join(folder, i), dtype='float32')
            self.ageefrazes.append(arrelem)
    
    def sayText(self, text :str = "exampletext"):
        try:
            print("Text der gesagt weren Soll:", text)
            response = self.polly.synthesize_speech(Text=text, OutputFormat="pcm", VoiceId="Vicki", SampleRate="16000")
            time.sleep(1)
        except(BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                
                retdate = stream.read()
                
                data = np.frombuffer(retdate, dtype=np.int16)
                sounddevice.playrec(data, 16000)

        else:
            print("Could not stream audio")

    def setgreeting(self, folder: str):
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        print(onlyfiles)
        self.greetingfrazes.clear()
        for i in onlyfiles:
            arrelem, self.standart = sf.read(join(folder, i), dtype='float32')
            self.greetingfrazes.append(arrelem)
    
