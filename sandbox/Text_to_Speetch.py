import sys
from urllib import response
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from numpy import dtype
import sounddevice as sd
import soundfile as sf
import numpy as np



polly = boto3.client('polly')

try:
    response = polly.synthesize_speech(Text="Mal schauen ob das hier passt", OutputFormat="pcm", VoiceId="Vicki", SampleRate="16000")

except(BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)

if "AudioStream" in response:
    with closing(response["AudioStream"]) as stream:

        data = np.frombuffer(stream.read(), dtype=int)
        sd.play(data, 9000)
        status = sd.wait() 

else:
    print("Could not stream audio")