#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import get_json, say
from random import choice

from os import path
import sys
try:
    from pocketsphinx import LiveSpeech, get_model_path
except ImportError:
    print("Error importing pocketsphinx")

DEBUG = True
KEY_WORDS_VALUE = 2
SEC_WORDS_VALUE = 1
EXC_WORDS_VALUE = -3

def get_intent(phrase,intents):
    """returns the most likely intention of the phrase out of the intents list"""

    words = phrase.split(" ")
    if DEBUG: print(words)

    #only do the hard part if we are going to find something
    if len(words) >= 2:
        #list for the points
        results = [0] * len(intents)    

        #index, value in iterable
        for i, intent in enumerate(intents):
            #check the mandatory words. at least one is needed
            #or none if no mandatory words where specified
            hasMandatoryWord = False
            if not intent["mandatory_words"]:
                hasMandatoryWord = True
            else:
                for mand_word in intent["mandatory_words"]:
                    if mand_word in words:
                        hasMandatoryWord = True
                        if DEBUG: print("found mandatory word")
                        break
            #for each intentions, only if we have a mandatory word
            #do we check the score
            if hasMandatoryWord:
                #foreach words, add or remove from the score
                for word in words:
                    if word in intent["key_words"]:
                        results[i]+=KEY_WORDS_VALUE
                    elif word in intent["secondary_words"]:
                        results[i]+=SEC_WORDS_VALUE
                    elif word in intent["excluded_words"]:
                        results[i]+=EXC_WORDS_VALUE

        if DEBUG: print(results)
        maxResult = max(results)

        #if smaller than two, we can't be sure of the request
        if maxResult >= 2:
            highest = intents[results.index(maxResult)]
            if DEBUG: print(highest["intent"])
            #return the intent in letters
            return choice(highest["answers"])

    return "Could not understand request"

def main():
    intents = get_json("intent.json")


    model_path = get_model_path()
    if DEBUG: print(model_path)

    print("Ready...")

    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=path.join(model_path, 'en-us'),
        lm=path.join(model_path, 'en-us.lm.bin'),
        dic=path.join(model_path, 'cmudict-en-us.dict'),
        mllr=path.join(model_path,'adapt-230517-1')
    )

    for phrase in speech:
        if str(phrase) == "stop":
            sys.exit(0)
        say(get_intent(str(phrase).lower(),intents))
        print("Listening...")

if __name__ == "__main__":
    main()