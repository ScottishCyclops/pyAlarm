import re

def get_informations(phrase,intent,debug=False):
    if intent["infos"]:
        words = phrase.split(" ")

        return {
            "report_weather":get_report_weather,
            "add_agenda":get_add_agenda,
            "set_alarm":get_set_alarm,

        }.get(intent["name"])(words)
            
    else:
        if debug: print("No words to seek for thie intention")
        return {}

def get_report_weather(words):
    infos = {"date":"today","time":"now","location":"current"}
    dateCases = [
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
    timeCases = [
        "now",
        "tonight",
        "morning",
        1,2,3,4,5,6,7,8,9,10,11,12,
    ]
    locationCases = [
        "home",
        "work",
    ]

    foundDate = False
    for date in dateCases:
        if str(date) in words:
            infos["date"] = date
            foundDate = True
            break

    foundTime = False
    for time in timeCases:
        if str(time) in words:
            infos["time"] = time
            foundTime = True
            break
    
    foundLocation = False
    for location in locationCases:
        if location in words:
            infos["location"] = location
            foundLocation = True
            break
    
    if not foundLocation:
        to_find = ""
        if "in" in words:
            to_find = "in"
        elif "at" in words:
            to_find = "at"
        
        if to_find != "":
            try:
                word = words[words.index(to_find)+1]
                #if none digit, to exlude "at 10 AM"
                if re.match(r"\D",word):
                    infos["location"] = word
            except IndexError(e):
                print("Last word was '{}'".format(to_find))
    return infos

def get_add_agenda(words):
    infos = {"date":"tomorrow","time":"entire_day","title":"new evenment"}
    return "retrieving agenda informations"

def get_set_alarm(words):
    infos = {"date":"tomorrow","hour":None,"minute":0}
    return "retrieving alarm informations"