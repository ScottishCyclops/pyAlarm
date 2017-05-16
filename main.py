#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from utils import Alarm, set_alarm
from wake import wake_me_up
import sys


def main():
    alarms = {

        0: set_alarm(0, 21,36),
        1: set_alarm(1, 21,57),
        2: set_alarm(2, 9,10),
        3: set_alarm(3, 9,10),
        4: set_alarm(4, 9,10),
        5: set_alarm(5, 9,10),
        6: set_alarm(6, 9,10),
        7: set_alarm(7, 16,0),
    }

    wake_me_up()
    sys.exit(0)

    alarm = Alarm(alarms,wake_me_up)
    alarm.start()

    while alarm.isRunning:
        if str(input()) == 'exit':
            alarm.stop()

if __name__ == '__main__':
    main()
