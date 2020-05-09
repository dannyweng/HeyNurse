#!/usr/bin/env python3

# Hey Nurse
# Author: Danny Weng
# Reference:
# https://github.com/dannyweng


# import modules
try:
    import argparse
    import locale
    import logging
    import platform
    import subprocess
    import sys
    from aiy.board import Board, Led
    from aiy.assistant import auth_helpers
    from aiy.assistant.library import Assistant
    from aiy.voice import tts
    from google.assistant.library.event import EventType
    #from aiy.cloudspeech import CloudSpeechClient
    from fitParse import googleFitAverage
    import fitParse
    from dateutil.parser import parse
    from datetime import datetime


# Any import errors print to screen and exit
except (Exception, error):
	print ('error')
	sys.exit(1)


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def power_off_pi():
    tts.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    tts.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))


def hey_nurse():
    tts.say('Hi, Danny')


def googleFitHeart(date, dataType):
    fitResponse = fitParse.googleFitAverage(date, dataType)
    tts.say(f"You're average heart rate on {fitDate} was {fitResponse}")


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
        
        # HEY NURSE Inquires here
        elif text.__contains__("heart" and "rate") and is_date(text, fuzzy=True) == True:
            assistant.stop_conversation()

            if is_date(text, fuzzy=True):
                whatIsTheDate = [parse(text, fuzzy_with_tokens=True)]
                # print(whatIsTheDate[0][0].strftime('%Y-%m-%d'))
                global fitDate
                fitDate = (whatIsTheDate[0][0].strftime('%Y-%m-%d'))
                # print(fitDate)
            else:
                fitDate = '2020-04-01'
                print('I didnt get a date')
            googleFitHeart(f'{fitDate}', 'Average heart rate (bpm)')
            print ("Yeyy, found the substring!")


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


def main():
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()