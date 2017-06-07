def get_informations(phrase, intent, debug=False):
    if intent["infos"]:
        words = phrase.split(" ")

        return {
            "report_weather":get_report_weather,
            "add_agenda":get_add_agenda,
            "set_alarm":get_set_alarm,

        }.get(intent["name"])(words)
            
    else:
        if debug: print("No words to seek for this intention")
        return {}


def get_report_weather(words):
    infos = {"date": "today", "time": "now", "location": "current"}
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
        1,2,3,4,5,6,7,8,9,10,11,12,
    ]
    location_cases = [
        "home",
        "work",
    ]

    found_date = False
    for date in date_cases:
        if str(date) in words:
            infos["date"] = date
            found_date = True
            break

    found_time = False
    for time in time_cases:
        if str(time) in words:
            infos["time"] = time
            found_time = True
            break

    found_location = False
    for location in location_cases:
        if location in words:
            infos["location"] = location
            found_location = True
            break

    if not found_location:
        if "in" in words:
            infos["location"] = words[words.index("in")+1]
        elif "at" in words:
            infos["location"] = words[words.index("at")+1]
    
    return infos

def get_add_agenda(words):
    infos = {"date":"tomorrow","time":"entire_day","title":"new evenment"}
    return "retrieving agenda informations"

def get_set_alarm(words):
    infos = {"date":"tomorrow","hour":None,"minute":0}
    return "retrieving alarm informations"