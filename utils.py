import datetime
import json
import re
import subprocess
import time
import urllib
from threading import Thread

from bs4 import BeautifulSoup

"""                                """
""" web page and string formatting """
"""                                """


def soft_cut_string(string: str, amount: int) -> str:
    """
    cuts a string at the next dot after the amount
    :param string: the string to cut
    :param amount: after how many characters to start cutting
    :return: the cut string
    """

    if len(string) > amount:
        next_dot_index = string.find(".", amount, -1)
        #+1 to include the dot
        return string[:next_dot_index + 1]
    else:
        #if the string is too short, nothing fancy to do
        return string


def remove_extra_whitespace(string: str) -> str:
    """
    removes the multiples whitespaces in a string and returns it
    :param string: the string to operate on
    :return: the string without extra whitespaces
    """

    return ' '.join(string.split())


def get_rand_wiki_page() -> dict:
    """
    returns a dict containing a page title, url and all the text from the paragraphs
    :return: dictionary containing the title, url and text from a random wikipedia page
    """

    req_url = "http://en.wikipedia.org/wiki/Special:Random"
    page = urllib.request.urlopen(req_url)
    dom = BeautifulSoup(page.read(), "html.parser")

    #wiki random performs a redirection, and we want to know the final page
    url = page.geturl()
    title = str(dom.find(id="firstHeading").string)

    paragraphs = dom.find_all("p")

    text = ""
    for p in paragraphs:
        text += p.get_text() + "\n"

    #remove references in wikipedia page, leave nothing instead
    text = re.sub(r"\[\d+\]", "", text)
    #remove parentheses, leave whitespace instead
    text = re.sub(r"\([^)]*\)", " ", text)
    #remove non ascii, leave whitespace instead
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    page.close()

    return {'title': title, 'url': url, 'text': text}


"""             """
""" other utils """
"""             """


def get_json(f: str) -> any:
    """
    returns the values contained in a json file
    :param f: name of the file to open
    :return: the content of the file as a python object
    """

    with open(f) as json_data:
        d = json.load(json_data)
    return d


def command(input_command: str) -> str:
    """
    executes a unix command in a proper way
    :param input_command: the command to run, like in a terminal
    :return: the output of the command, might be None
    """

    p = subprocess.Popen(input_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return str(output)


def say(text: str) -> str:
    """
    says a text using festival tts
    :param text: the text to say out loud
    :return: the output of the command executed
    """

    return command("echo \"" + text + "\" | festival --tts")


#TODO: implement
def get_word_after(phrase, words, match=None):
    """under development"""

    to_find = ""
    if "in" in words:
        to_find = "in"
    elif "at" in words:
        to_find = "at"

    if to_find != "":
        try:
            word = words[words.index(to_find) + 1]
            #if none digit, to exclude "at 10 AM"
            if re.match(r"\D", word):
                return word
        except IndexError:
            print("Last word was '{}'".format(to_find))


"""            """
""" date utils """
"""            """


class Alarm(Thread):
    def __init__(self, alarms: iter, func: any):
        """
        alarm class based on the Thread class that runs and rings the alarms given
        :param alarms: the list of alarms to ring
        :param func: the function to call when ringing an alarm
        """

        super(Alarm, self).__init__()
        self.alarms = alarms
        self.func = func
        self.isRunning = False

    def run(self):
        self.isRunning = True
        try:
            next_alarm = choose_next_alarm(self.alarms)
            while self.isRunning:
                t1 = get_date()
                print_date(t1)
                '''if the alarm passed and we are the day it was supposed to pass'''
                if has_alarm_passed(next_alarm) \
                        and next_alarm['weekday'] == get_weekday_number(t1):

                    '''run the given function to wake up'''
                    self.func()

                    next_alarm = choose_next_alarm(self.alarms)

                time.sleep(1)

        except KeyboardInterrupt:
            #TODO: verify what else can fail
            self.stop()
            return

    def stop(self):
        self.isRunning = False


def get_date():
    """wrapper for datetime.now"""

    return datetime.datetime.now()


def get_weekday_number(t):
    """wrapper for datetime weekday"""

    return datetime.datetime.weekday(t)


def print_date(t):
    """formats a date and prints it"""

    print("{0} {1} {2} {3:02}:{4:02}:{5:02}".format(get_weekday_name(get_weekday_number(t)),
                                                    t.day,
                                                    get_month_name(t.month),
                                                    t.hour,
                                                    t.minute,
                                                    t.second))


def get_weekday_name(d: int) -> str:
    """
    returns a string from a weekday number
    :param d: day of the week (0-6)
    :return: the day of the week as a word
    """

    return {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
        7: "Invalid"
    }.get(d, 7)


def get_month_name(m: int) -> str:
    """
    returns a string from a month number
    :param m: month (1-12)
    :return: the month as a word
    """

    return {
        1:  "January",
        2:  "February",
        3:  "March",
        4:  "April",
        5:  "May",
        6:  "June",
        7:  "July",
        8:  "August",
        9:  "September",
        10: "October",
        11: "November",
        12: "December",
        13: "Invalid",
    }.get(m, 13)


def set_alarm(weekday: int, hour: int, minute: int) -> dict:
    """
    returns a dict containing the weekday the hour and the minute of an alarm
    :param weekday: day of the week (0-6)
    :param hour: hour of the day (0-23)
    :param minute: minute of the hour (0-59)
    :return: a dictionary containing the given information
    """

    return {"weekday": weekday, "hour": hour, "minute": minute}


def has_alarm_passed(alarm: dict) -> bool:
    """
    checks if an alarm time has passed, not if it's day has
    :param alarm: the alarm dictionary created with set_alarm
    :return: whether the alarm's time was before the current time
    """

    passed = False
    t = get_date()
    if alarm["hour"] < t.hour:
        passed = True
    elif alarm['hour'] == t.hour:
        if alarm['minute'] <= t.minute:
            passed = True
    return passed


def choose_next_alarm(alarms: iter) -> dict:
    """
    returns the alarm for this day of the week. if the alarm has passed, take the one from the next day
    :param alarms: all the alarms created with set_alarm
    :return: the next alarm, for this day or the next one
    """

    t = get_date()
    #get the alarm of this week's day
    next_alarm = alarms.get(get_weekday_number(t), 7)

    if has_alarm_passed(next_alarm):
        #if it has already passed, get the one from the next week day, within 0-6 range
        next_alarm = alarms.get((get_weekday_number(t) + 1) % 7, 7)

    return next_alarm


def print_alarm(alarm: dict):
    """
    prints the basic information of the alarm
    :param alarm: an alarm constructed with set_alarm
    """

    day = get_weekday_name(alarm['weekday'])
    print("Alarm: {0} à {1:02}:{2:02}".format(day, alarm["hour"], alarm["minute"]))

