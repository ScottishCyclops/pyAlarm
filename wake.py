import random

from utils import get_rand_wiki_page, get_date, remove_extra_whitespace, soft_cut_string, get_json, get_weekday_name, \
    get_weekday_number, say

LENGTH = 1500


def wake_me_up():
    """
    function to execute to wake up. reads a wikipedia article then gives useful information
    """

    t = get_date()

    #getting article
    page = get_rand_wiki_page()
    while len(page["text"]) < LENGTH:
        print("too short")
        page = get_rand_wiki_page()

    article = page["title"] + ". " + remove_extra_whitespace(soft_cut_string(page["text"], LENGTH).replace("\n", " "))

    #loading parameters
    d = get_json("wake_up.json")

    #constants for now
    temp = "25"
    conditions = "sunny"
    planning = "shopping, going to school"

    #none constant info
    weekday = get_weekday_name(get_weekday_number(t))

    intro = random.choice(d["intro"])
    outro = random.choice(d["outro"])
    salute = random.choice(d["salute"]).format(d["user_name"])
    weather = random.choice(d["weather"]).format(temp, d["temp_scale"], conditions)
    day = random.choice(d["day"]).format(weekday, planning)

    text = " ".join([intro, article, outro, salute, weather, day])

    print(text)
    say(text)

    end_time = get_date()
    total_time = end_time - t
    print(total_time)
