#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import time
import threading
import argparse
import os
import led
import subprocess
from phue import Bridge
from led.matrixled import MatrixLed, get_led
from led.ledrunner import LedRunner
from snowboy.wakeword import Wakeword
from stream import Recognizer
from matcher.matcher import PhraseMatcher

LED_GREEN = get_led(green=20)
LED_YELLOW = get_led(red=20, green=20)
LED_RED = get_led(red=20)
LED_STANDBY = get_led(blue=10)

class StandbyLoop(LedRunner):
    def __loop(self):
        index = 0
        while self.running:
            led.single(LED_STANDBY, index)
            time.sleep(1)
            index = (index + 1) % 35

    def start(self):
        self.stop()
        self.running = True
        self.thread = threading.Thread(target=self.__loop)
        self.thread.start()

class HueController:
    def __init__(self, ip, username=None, config=None):
        self.bridge = Bridge(ip, username, config)
        self.bridge.connect()

    def toggle(self, lights, is_lit):
        all_lights = [lights] if type(lights) is not list else lights
        [self.bridge.set_light(light, 'on', is_lit) for light in all_lights]


led = MatrixLed()
runner = LedRunner()
speech = Recognizer('FI-fi')
standby_loop = StandbyLoop()
ACTIONS = {
    'Valot päälle': (lambda: hue.toggle([1, 2], True)),
    'Valot pois': (lambda: hue.toggle([1, 2], False)),
    'Sytytä valot': (lambda: hue.toggle([1, 2], True)),
    'Sammuta valot': (lambda: hue.toggle([1, 2], False)),
    'Kaiuttimet': (lambda: subprocess.run(['irsend', 'SEND_ONCE', 'AUDIOPRO_T12', 'KEY_POWER'])),
    'Kaiutin': (lambda: subprocess.run(['irsend', 'SEND_ONCE', 'AUDIOPRO_T12', 'KEY_POWER'])),
    'Kajarit': (lambda: subprocess.run(['irsend', 'SEND_ONCE', 'AUDIOPRO_T12', 'KEY_POWER']))
    }
matcher = PhraseMatcher(ACTIONS.keys())

def make_action(command):
    if command is not None:
        print(command)
        runner.once(led.loading_bar, LED_GREEN)
        transcript = command.get('transcript')
        action = matcher.match(transcript)
        ACTIONS.get(action)()
    else:
        runner.once(led.solid, LED_RED)
    time.sleep(1)

def wakeword_handler(wakeword_model):
    standby_loop.stop()
    runner.once(led.solid, LED_YELLOW)
    command = speech.listen(6)
    make_action(command)
    standby_loop.start()

def main():
    led.connect()
    standby_loop.start()

    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='Philips HUE bridge ip')
    parser.add_argument('--username', help='Philips HUE bridge username')
    parser.add_argument('--config', help='Path to Philips HUE bridge config file', metavar='CONFIG_PATH')
    args = parser.parse_args()

    global hue
    hue = HueController(ip=args.ip, username=args.username, config=args.config)

    try:
        while True:
            print('Listening...')
            wakeword = Wakeword(wakeword_handler, 0.4)
            wakeword.listen()
    except KeyboardInterrupt:
        print('Bye!')
        wakeword.stop()

    standby_loop.stop()
    runner.once(led.solid)

if __name__ == '__main__':
    main()

