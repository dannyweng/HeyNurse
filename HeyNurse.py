import argparse
import locale
import logging

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts

import logging
import platform
import subprocess
import sys

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts

class Myassistant:

    def __init__(self):
        self.interrupted=False
        self.can_start_conversation=False
        self.assistant=None
        self.sensitivity = [0.5]*len(models)
        self.callbacks = [self.detected]*len(models)
        self.detector = snowboydecoder.HotwordDetector(models, sensitivity=self.sensitivity)
        self.mutestatus=False
        self.interpreter=False
        self.interpconvcounter=0
        self.interpcloudlang1=language
        self.interpttslang1=translanguage
        self.interpcloudlang2=''
        self.interpttslang2=''
        self.singleresposne=False
        self.singledetectedresponse=''
        self.t1 = Thread(target=self.start_detector)
        if GPIOcontrol:
            self.t2 = Thread(target=self.pushbutton)
        if configuration['MQTT']['MQTT_Control']=='Enabled':
            self.t3 = Thread(target=self.mqtt_start)
        if irreceiver!=None:
            self.t4 = Thread(target=self.ircommands)
        if configuration['ADAFRUIT_IO']['ADAFRUIT_IO_CONTROL']=='Enabled':
            self.t5 = Thread(target=self.adafruit_mqtt_start)

    def power_off_pi(self):
        tts.say('Good bye!')
        subprocess.call('sudo shutdown now', shell=True)


    def reboot_pi(self):
        tts.say('See you in a bit!')
        subprocess.call('sudo reboot', shell=True)


    def say_ip(self):
        ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
        tts.say('My IP address is %s' % ip_address.decode('utf-8'))


    def hey_nurse(self):
        tts.say('Hi, Danny')


    def process_event(assistant, led, event):
        logging.info(event)
        if event.type == EventType.ON_START_FINISHED:
            led.state = Led.BEACON_DARK  # Ready.
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED: #Hot Word activation 'OK Google'
            led.state = Led.ON  # Listening.
        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print('You said:', event.args['text'])
            text = event.args['text'].lower()
            if text == 'power off':
                assistant.stop_conversation()
                power_off_pi()
            elif text == 'reboot':
                assistant.stop_conversation()
                reboot_pi()
            elif text == 'ip address':
                assistant.stop_conversation()
                say_ip()
            elif text == 'hey nurse':
                assistant.stop_conversation()
                hey_nurse()
            else: #debug
                #print('debug: ' + text)
                print(EventType.ON_RENDER_RESPONSE)
        elif event.type == EventType.ON_END_OF_UTTERANCE:
            led.state = Led.PULSE_QUICK  # Thinking.
        elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
            or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
            or event.type == EventType.ON_NO_RESPONSE):
            led.state = Led.BEACON_DARK  # Ready.
        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            sys.exit(1)


    def main(self):
        logging.basicConfig(level=logging.INFO)
        #logging.basicConfig(level=logging.DEBUG)

        credentials = auth_helpers.get_assistant_credentials()
        with Board() as board, Assistant(credentials) as assistant:
            for event in assistant.start():
                process_event(assistant, board.led, event)


if __name__ == '__main__':
    try:
        Myassistant.main()
    except Exception as error:
        logging.exception(error)