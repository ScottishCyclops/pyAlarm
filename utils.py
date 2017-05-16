#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import json
import os
import re
import subprocess
import time
import urllib
from threading import Thread

from bs4 import BeautifulSoup

"""          """
"""web page and string formating"""
"""          """

"""cuts a string at the next dot after the amount"""
def soft_cut_string(string,amount):
    if len(string) > amount:
        nextDotIndex = string.find(".",amount,-1)
        return string[:nextDotIndex+1]
    else:
        return string

def remove_extra_whitespace(string):
    return ' '.join(string.split())

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+',' ', text)

"""returns a dict containing a page title, url and all the text from the <p>'s in the page"""
def get_rand_wiki_page():
    reqUrl = 'http://en.wikipedia.org/wiki/Special:Random'
    page = urllib.request.urlopen(reqUrl)
    dom = BeautifulSoup(page.read(), 'html.parser')

    url = page.geturl()
    title = dom.find(id='firstHeading').string

    paragraphs = dom.find_all('p')
    text = ''
    for p in paragraphs:
        text+=p.get_text()+'\n'
    #remove references in wikipage
    text = re.sub(r"\[\d+\]","",text)
    #remove parentheses
    text = re.sub(r"\([^)]*\)"," ",text)
    #remove non ascii
    text = remove_non_ascii(text)

    page.close()

    return {'title':title,'url':url,'text':text}


"""          """
"""other utils"""
"""          """

def get_json(f):
    with open(f) as json_data:
        d = json.load(json_data)
    return d

def execute_unix(inputcommand):
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
   return output

def say(text):
    execute_unix("echo \""+text+"\" | festival --tts")

"""          """
"""date utils"""
"""          """

class Alarm(Thread):
    def __init__(self,alarms,function):
        super(Alarm, self).__init__()
        self.alarms = alarms
        self.function = function
        self.isRunning = False

    def run(self):
        self.isRunning = True
        try:
            nextAlarm = choose_next_alarm(self.alarms)
            while self.isRunning:
                t1 = get_date()
                print_date(t1)
                '''if the alams passed and we are the day it was supposed to pass'''
                if has_alarm_passed(nextAlarm) and nextAlarm['weekday'] == get_weekday_number(t1):

                    '''run the given function to wake up'''
                    self.function()

                    nextAlarm = choose_next_alarm(self.alarms)

                time.sleep(1)

        except:
             self.isRunning = False
            return
    def stop(self):
        self.isRunning = False

def get_date():
    return datetime.datetime.now()

def get_weekday_number(t):
    return datetime.datetime.weekday(t)

def print_date(t):
    print("{0} {1} {2} {3:02}:{4:02}:{5:02}".format(get_weekday_name(get_weekday_number(t)),t.day,get_month_name(t.month), t.hour,t.minute,t.second))

def get_weekday_name(t):
    return {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
        7: 'Invalid'
    }.get(t,7)

def get_month_name(t):
    return {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
        13: 'Invalid',
    }.get(t,13)

def set_alarm(weekday, hour,minute):
    return {'weekday': weekday, 'hour': hour, 'minute': minute}

def has_alarm_passed(alarm):
    passed = False
    t = get_date()
    if alarm['hour'] < t.hour:
        passed = True
    elif alarm['hour'] == t.hour:
        if alarm['minute'] <= t.minute:
            passed = True
    return passed

def choose_next_alarm(alarms):
    t = get_date()
    nextAlarm = alarms.get(get_weekday_number(t),7)

    if has_alarm_passed(nextAlarm):
        nextAlarm = alarms.get((get_weekday_number(t)+1)%7,7)

    return nextAlarm

def print_alarm(alarm):
    day = get_weekday_name(alarm['weekday'])
    print('Réveil: {0} à {1:02}:{2:02}'.format(day,alarm['hour'],alarm['minute']))
