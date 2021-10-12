#!/usr/bin/env python3

import logging
import locale
import argparse
import aiy.voice.audio
from aiy.board import Board
from aiy.cloudspeech import CloudSpeechClient
from gpiozero import Servo
from time import sleep

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('trick or treat',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    recognizer = CloudSpeechClient()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)

    servo = Servo(26)
    servo.min()

    with Board() as board:
        while True:
            board.button.wait_for_press()
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = recognizer.recognize(language_code=args.language,
                                        hint_phrases=hints)
            if text is None:
                continue
            else:
                print('You said ', text)
                if 'trick or treat' in text:
                    print('max!')
                    servo.max()
                    sleep(1)
                    servo.min()

if __name__ == '__main__':
    main()
