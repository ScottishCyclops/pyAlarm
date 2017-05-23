#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import get_json
from random import choice

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
            #foreach words
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
            #return the intent in letters
            return highest["intent"]

    return "Could not understand request"

def main():
    intents = get_json("intent.json")
    phrase = "AH"
    while phrase != "stop":
        #we put everything to lower for comparaisons
        phrase = input("Phrase: ").lower()

        print(get_intent(phrase,intents))

if __name__ == "__main__":
    main()