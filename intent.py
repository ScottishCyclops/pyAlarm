KEY_WORDS_VALUE = 2
SEC_WORDS_VALUE = 1
EXC_WORDS_VALUE = -3
MIN_RESULT_THRESHOLD = 2


def get_intent(phrase: str, intents: iter, debug: bool = False) -> dict:
    """
    returns the most likely intention of the phrase out of the intents list
    :param phrase: the phrase out of which we want to determine the intent
    :param intents: the list of intents to choose from
    :param debug: optional switch that prints debug information if on
    :return: a dictionary containing the intention, or an empty one if failed
    """

    words = phrase.split(" ")
    if debug:
        print(words)

    #only search intent if at least 2 words
    if len(words) >= 2:
        #list for the points
        results = [0] * len(intents)

        #format : for index, value in iterable:
        for i, intent in enumerate(intents):
            #check the mandatory words. at least one is needed
            #or none if no mandatory words where specified
            has_mandatory_word = False
            if not intent["mandatory_words"]:
                has_mandatory_word = True
            else:
                for mandatory_word in intent["mandatory_words"]:
                    if mandatory_word in words:
                        has_mandatory_word = True
                        if debug:
                            print("found mandatory word")
                        break

            #for each intentions, only if we have a mandatory word
            if has_mandatory_word:
                #foreach words, add or remove from the score
                for word in words:
                    if word in intent["key_words"]:
                        results[i] += KEY_WORDS_VALUE
                    elif word in intent["secondary_words"]:
                        results[i] += SEC_WORDS_VALUE
                    elif word in intent["excluded_words"]:
                        results[i] += EXC_WORDS_VALUE

        if debug:
            print(results)
        max_result = max(results)

        if max_result >= MIN_RESULT_THRESHOLD:
            most_likely_intent = intents[results.index(max_result)]
            if debug:
                print(most_likely_intent["intent"])
            return most_likely_intent

    if debug:
        print("No intent found")
    return {}

