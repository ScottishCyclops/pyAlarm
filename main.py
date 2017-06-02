#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import Alarm, set_alarm, get_json
from intent import get_intent
from wake import wake_me_up
import sys


def main():
    intents = get_json("intent.json")
    while True:
        try:
            phrase = input("Phrase: ")
            print(get_intent(str(phrase).lower(),intents))
        except KeyboardInterrupt:
            sys.exit(0)

    '''
    
    alarm_tot = [6,5]
    alarm_normal = [6,42]
    alarm_tard = [7,5]
    alarm_weekend = [9,30]

    alarms = {
        0: set_alarm(0, *alarm_normal),
        1: set_alarm(1, *alarm_normal),
        2: set_alarm(2, *alarm_tot),
        3: set_alarm(3, *alarm_tard),
        4: set_alarm(4, *alarm_normal),
        5: set_alarm(5, *alarm_weekend),
        6: set_alarm(6, *alarm_weekend),
    }

    alarm = Alarm(alarms,wake_me_up)
    alarm.start()

    while alarm.isRunning:
        if str(input()) == 'exit':
            alarm.stop()
            '''


if __name__ == '__main__':
    main()
