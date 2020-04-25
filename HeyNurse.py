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


def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
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
    logging.basicConfig(level=logging.DEBUG)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()



'''

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'turn on the light' in text:
                board.led.state = Led.ON
            elif 'turn off the light' in text:
                board.led.state = Led.OFF
            elif 'blink the light' in text:
                board.led.state = Led.BLINK
            # Our new command:
            if 'repeat after me' in text:
                # Remove "repeat after me" from the text to be repeated
                to_repeat = text.replace('repeat after me', '', 1)
                aiy.voice.tts.say(to_repeat)
            
            # Hey Nurse commands
            if 'hey nurse' in text:
                aiy.voice.tts.say('hi danny')

            elif 'goodbye' in text:
                break

if __name__ == '__main__':
    main()


def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye',
                'repeat after me',
                'hey nurse')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language


def process_event(assistant, led, event):
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            else:

                logging.info('You said: "%s"' % text)
                text = text.lower()
                if 'turn on the light' in text:
                    board.led.state = Led.ON
                elif 'turn off the light' in text:
                    board.led.state = Led.OFF
                elif 'blink the light' in text:
                    board.led.state = Led.BLINK
                elif 'goodbye' in text:
                    break
                # Our new command:
                if 'repeat after me' in text:
                    # Remove "repeat after me" from the text to be repeated
                    to_repeat = text.replace('repeat after me', '', 1)
                    aiy.voice.tts.say(to_repeat)
                
                # Hey Nurse commands
                if 'hey nurse' in text:
                    aiy.voice.tts.say('hi danny')
                    #logging.info(event)
                    #print(event.type)
                    #print(EventType)

                    if event.type == EventType.ON_MUTED_CHANGED:
                        led.state = Led.BEACON_DARK  # Ready.
                        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
                    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
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
                    elif event.type == EventType.ON_END_OF_UTTERANCE:
                        led.state = Led.PULSE_QUICK  # Thinking.
                    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
                        or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
                        or event.type == EventType.ON_NO_RESPONSE):
                        led.state = Led.BEACON_DARK  # Ready.
                    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
                        sys.exit(1)
                continue





                logging.info(event)


def main():
    logging.basicConfig(level=logging.INFO)

    #logging.basicConfig(level=logging.DEBUG)


    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            print(event)
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()

'''