from queue import Queue, Full
from threading import Thread
from configparser import ConfigParser

import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

CHUNK = 1024

BUF_MAX_SIZE = CHUNK * 10

q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

audio_source = AudioSource(q, True, True)

CREDENTIALS_FILENAME = 'ibm-credentials.env'

DUMMY_SECTION_NAME = 'dummy'

with open(CREDENTIALS_FILENAME) as f:
    file_content = f'[{DUMMY_SECTION_NAME}]\n' + f.read()

config_parser = ConfigParser()
config_parser.read_string(file_content)
api_key = config_parser[DUMMY_SECTION_NAME]['SPEECH_TO_TEXT_APIKEY']
url = config_parser[DUMMY_SECTION_NAME]['SPEECH_TO_TEXT_URL']

authenticator = IAMAuthenticator(api_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.result_index = -1

    def on_transcription(self, transcript):
        pass

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        pass

    def on_data(self, data):
        final = data['results'][0]['final']
        transcript = data['results'][0]['alternatives'][0]['transcript']
        if final:
            end = "\n"
        else:
            end = "\r"
        print(transcript, end=end)

    def on_close(self):
        print("Connection closed")

def recognize_using_weboscket(*args):
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             model='ja-JP_BroadbandModel',
                                             interim_results=True)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=pyaudio_callback,
    start=False
)

print("Enter CTRL+C to end recording...")
stream.start_stream()

try:
    recognize_thread = Thread(target=recognize_using_weboscket, args=())
    recognize_thread.start()

    while True:
        pass
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()
