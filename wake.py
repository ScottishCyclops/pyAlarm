#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random

from utils import *

LENGTH = 1500

def wake_me_up():
    """getting article"""
    page = get_rand_wiki_page()
    while len(page['text']) < LENGTH:
        print('too short')
        page = get_rand_wiki_page()

    article = page['title'] + ". " + remove_extra_whitespace(soft_cut_string(page['text'],LENGTH).replace("\n"," "))

    """loading parameters"""
    d = get_json('wake_up.json')

    """constantes for now"""
    temp = '25'
    conditions = 'sunny'
    planning = "shopping, going to school"
    
    """none constante info"""
    weekday = get_weekday_name(get_weekday_number(get_date()))

    intro = random.choice(d['intro'])
    outro = random.choice(d['outro'])
    salute = random.choice(d['salute']).format(d['user_name'])
    weather =  random.choice(d['weather']).format(temp,d['temp_scale'],conditions)
    day = random.choice(d['day']).format(weekday,planning)

    text = " ".join([intro,article,outro,salute,weather,day])

    print(text)
    say(text)
