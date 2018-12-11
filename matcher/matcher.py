from fuzzywuzzy import process
class PhraseMatcher:
    def __init__(self, phrases=[], threshold=0):
        self.phrases = phrases
        self.threshold = threshold

    def match(self, phrase):
        if len(self.phrases) is 0 or phrase is None:
            return phrase
        match = process.extractOne(phrase, self.phrases)
        if match[1] >= self.threshold:
            return match[0]
        return None
