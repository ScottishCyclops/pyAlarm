import re


def get_information(phrase: str, intent: dict, debug: bool = False) -> dict:
    """
    extract meaningful information from a phrase based on an intent
    :param phrase: the phrase to extract from
    :param intent: the intention of the phrase returned by intent.get_intent
    :param debug: optional switch that prints debug information if on
    :return: a dictionary containing the gathered information, or an empty one if failed
    """
    if intent["info"]:
        words = phrase.split(" ")

        info = {
            "report_weather": get_report_weather,
            "add_agenda":     get_add_agenda,
            "set_alarm":      get_set_alarm,

        }.get(intent["name"], get_default)(words)

        return info if info else {}

    else:
        if debug:
            print("No words to seek for this intention")
        return {}


def get_default(param: dict) -> any:
    """
    default function called when an error occurred trying to call a specialized function
    :param param: the params given to us. they have no use
    :return: an empty dict
    """
    print("An error occurred while calling the specialized extraction function")
    return None


def get_report_weather(words: iter) -> any:
    """
    specialized function that extracts information for weather reports
    :param words: list of words
    :return: the gathered information, or None if failed
    """
    info = {"date": "today", "time": "now", "location": "current"}
    date_cases = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "today",
        "tomorrow",
        "yesterday",
    ]
    time_cases = [
        "now",
        "tonight",
        "morning",
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    ]
    location_cases = [
        "home",
        "work",
    ]

    found_date = False
    for date in date_cases:
        if str(date) in words:
            info["date"] = date
            found_date = True
            break

    found_time = False
    for time in time_cases:
        if str(time) in words:
            info["time"] = time
            found_time = True
            break

    found_location = False
    for location in location_cases:
        if location in words:
            info["location"] = location
            found_location = True
            break

    if not found_location:
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
                    info["location"] = word
            except IndexError:
                print("'{}' was the last word. Next index not valid".format(to_find))
    return info


def get_add_agenda(words):
    """under development"""
    info = {"date": "tomorrow", "time": "entire_day", "title": "new event"}
    return "retrieving agenda information"


def get_set_alarm(words):
    """under development"""
    info = {"date": "tomorrow", "hour": None, "minute": 0}
    return "retrieving alarm information"
