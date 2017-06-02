from random import choice

def get_important_words(phrase,intent):
    words = phrase.split(" ")
    return choice(words)