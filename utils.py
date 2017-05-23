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

def soft_cut_string(string,amount):
    """cuts a string at the next dot after the amount"""
    if len(string) > amount:
        nextDotIndex = string.find(".",amount,-1)
        return string[:nextDotIndex+1]
    else:
        return string

def remove_extra_whitespace(string):
    """removes the multiples whitespaces in a string and returns it"""
    return ' '.join(string.split())

def get_rand_wiki_page():
    """returns a dict containing a page title, url and all the text from the paragraphs"""
    reqUrl = 'http://en.wikipedia.org/wiki/Special:Random'
    page = urllib.request.urlopen(reqUrl)
    dom = BeautifulSoup(page.read(), 'html.parser')

    url = page.geturl()
    title = dom.find(id='firstHeading').string

    paragraphs = dom.find_all('p')
    text = ''
    for p in paragraphs:
        text+=p.get_text()+'\n'
    #remove references in wikipage, leave nothing
    text = re.sub(r"\[\d+\]","",text)
    #remove parentheses, leave whitespace instead
    text = re.sub(r"\([^)]*\)"," ",text)
    #remove non ascii, leave whitespace instead
    text = re.sub(r'[^\x00-\x7F]+'," ", text)

    page.close()

    return {'title':title,'url':url,'text':text}


"""          """
"""other utils"""
"""          """

def get_json(f):
    """returns the values contained in a json file"""
    with open(f) as json_data:
        d = json.load(json_data)
    return d

def execute_unix(inputcommand):
    """executes a unix command in a proper way"""
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
   return output

def say(text):
    """says a text using festival tts"""
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
    """wrapper for datetime now"""
    return datetime.datetime.now()

def get_weekday_number(t):
    """wrapper for datetime weekday"""
    return datetime.datetime.weekday(t)

def print_date(t):
    """formats a date and prints it"""
    print("{0} {1} {2} {3:02}:{4:02}:{5:02}".format(get_weekday_name(get_weekday_number(t)),t.day,get_month_name(t.month), t.hour,t.minute,t.second))

def get_weekday_name(t):
    """returns a string from a weekday number (0-6)"""
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
    """returns a string from a month number (1-12)"""
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
    """returns a dict containing the weekday (0-6) the mour and the minute of an alarm"""
    return {'weekday': weekday, 'hour': hour, 'minute': minute}

def has_alarm_passed(alarm):
    """checks if an alarm time has passed, not day"""
    passed = False
    t = get_date()
    if alarm['hour'] < t.hour:
        passed = True
    elif alarm['hour'] == t.hour:
        if alarm['minute'] <= t.minute:
            passed = True
    return passed

def choose_next_alarm(alarms):
    """returns the alarm for this day of the week. if the alarm has passed, take the one from the next day"""
    t = get_date()
    nextAlarm = alarms.get(get_weekday_number(t),7)

    if has_alarm_passed(nextAlarm):
        nextAlarm = alarms.get((get_weekday_number(t)+1)%7,7)

    return nextAlarm

def print_alarm(alarm):
    """prints the basic informations of the alarm"""
    day = get_weekday_name(alarm['weekday'])
    print('Réveil: {0} à {1:02}:{2:02}'.format(day,alarm['hour'],alarm['minute']))
