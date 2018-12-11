from snowboy.snowboydecoder import HotwordDetector
from glob import glob
import time
import os
import signal

def _get_models(base_path):
    dirPath = base_path + "/models/*"
    return glob(dirPath + ".pmdl") + glob(dirPath + ".umdl")

class Wakeword:
    def __init__(self, callback, sensitivity=0.5):
        #signal.signal(signal.SIGINT, lambda signal, frame: self.__stop())
        self.__interrupted = False
        self.__callback = callback
        self.__models = _get_models(os.path.dirname(__file__))
        self.__detector = HotwordDetector(self.__models, sensitivity=len(self.__models)*[sensitivity])
        
    def stop(self):
        self.__interrupted = True
        self.__detector.terminate()
        
    def __detected_callback(self, hotword_number):
        self.stop()
        time.sleep(.05)
        self.__callback(os.path.basename(self.__models[hotword_number - 1]))
        
    def listen(self):
        self.__detector.start(detected_callback=self.__detected_callback,
                            interrupt_check=lambda: self.__interrupted,
                            sleep_time=0.03)
        