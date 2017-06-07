from os import path
import sys

try:
    from pocketsphinx import LiveSpeech, get_model_path
except ImportError:
    print("Error importing pocketsphinx")

from information import get_information
from intent import get_intent
from utils import Alarm, get_json, set_alarm, say
from wake import wake_me_up


def main():
    intents = get_json("intent.json")

    while True:
        try:
            phrase = str(input("Phrase: ")).lower()
            if phrase == "stop":
                sys.exit(0)
            elif phrase != "":
                intent = get_intent(phrase, intents, True)
                if intent:
                    print(get_information(phrase, intent))
        except KeyboardInterrupt:
            sys.exit(0)


'''
    #old test code to clean up

    intents = get_json("intent.json")
    lang = "fr"

    model_path = get_model_path()

    print("Ready...")

    speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=path.join(model_path, lang),
            lm=path.join(model_path, '{}.lm.bin'.format(lang)),
            dic=path.join(model_path, 'cmudict-{}.dict'.format(lang)),
            #mllr=path.join(model_path,'adapt-3')
    )

    for phrase in speech:
        ah
    
    alarm_early = [6,5]
    alarm_normal = [6,42]
    alarm_late = [7,5]
    alarm_weekend = [9,30]

    alarms = {
        0: set_alarm(0, *alarm_normal),
        1: set_alarm(1, *alarm_normal),
        2: set_alarm(2, *alarm_early),
        3: set_alarm(3, *alarm_late),
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

if __name__ == "__main__":
    main()

