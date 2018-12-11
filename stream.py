#!/usr/bin/env python
import threading
import subprocess
import wave
import time
import io
import alsaaudio, audioop
from functools import partial
from six.moves import queue
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

RATE = 16000
CHUNK = 1600;

class MicStream:
    def __init__(self, timeout):
        self.buff = queue.Queue()
        self.closed = True
        self.timeout = timeout

    def __enter__(self):
        self.closed = False
        self.record_thread = threading.Thread(target = self.record_proc)
        self.record_thread.start()
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        self.record_thread.join()

    def fill_buffer(self, in_data):
        """Continuously collect data from the audio stream, into the buffer."""
        self.buff.put(in_data)
        return None

    def stop(self):
        self.closed = True

    def record_proc(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)

        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(512)

        start_time = time.time()
        print('Starting speech recognition...')
        while True:
            elapsed = time.time() - start_time
            if elapsed > self.timeout or self.closed:
                print('Finished recognition after %s' % time.strftime('%H:%M:%S', time.gmtime(elapsed)))
                break
            l, data = inp.read()
            if l:
                self.fill_buffer(data)
        self.fill_buffer(None)

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            counter = 0
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                    counter += 1
                except queue.Empty:
                    break

            yield b''.join(data)
            
class Recognizer:
    def __init__(self, lang):
        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
                        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=RATE,
                        language_code=lang)
                        
    def __wait_for_response(self, responses):
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            if result.is_final:
                return {'transcript': result.alternatives[0].transcript, 'confidence': result.alternatives[0].confidence}
        
    def listen(self, timeout=5):
        try:
            with MicStream(timeout) as stream:
                generator = stream.generator()
                requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
                responses = self.client.streaming_recognize(
                    types.StreamingRecognitionConfig(config=self.config, single_utterance=True), 
                    requests)
                return self.__wait_for_response(responses)
        except:
            print('Unknown error with grpc channel')
            return None

def main():
    recognizer = Recognizer('fi-FI')
    print(recognizer.listen())

if __name__ == '__main__':
    main()
