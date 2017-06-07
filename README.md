# pyAlarm

This is a regroupement of tests regarding a personal assistant.

At first, it was only supposed to be an alarm, that explains the name, I guess.

## Files

### test/tts-test.py

this files is used to test multiple text to speech engines at once

### information.py

this file contains a function that extracts useful information from a phrase, based on an intention

### intent.json

this file contains all the intentions that can be recognized by intent.py

### intent.py

this file contains a function that fines an intent based on a phrase

### main.py

this file is the entry point of the program.
It is mostly used for testing purposes as of right now

### utils.py

this file contains a lot of utility functions for the others files

### wake_up.json

this file contains the sentences to choose from when building the wake up phrase

### wake.py

this file contains the function to execute to wake up.
I builds a string containing useful information and a wikipedia article, and reads it out loud



_Warning: Project made for fun only!_