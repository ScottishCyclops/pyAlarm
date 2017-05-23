#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import get_json
from random import choice

def get_intent(phrase,intents):
    #for each intent, find the probability
    #return the highest probability

    words = phrase.split(" ")
    print(words)
    
    if len(words) >= 2:
        results = [0] * len(intents)    

        for i, intent in enumerate(intents):
            for word in words:
                if word in intent["key_words"]:
                    results[i]+=2
                elif word in intent["secondary_words"]:
                    results[i]+=1
                elif word in intent["excluded_words"]:
                    results[i]-=3

        print(results)
        maxResult = max(results)
        if maxResult >= 2:
            highest = intents[results.index(maxResult)]
            #phrase = choice(highest["answers"])
            return highest["intent"]

    return "Could not understand request"
        

def main():
    intents = get_json("intent.json")
    #phrase = "Remind me to get to the party tomorrow at 5".lower()
    phrase = "AH"
    while phrase != "stop it":
        phrase = input("Phrase: ").lower()

        print(get_intent(phrase,intents))


if __name__ == "__main__":
    main()