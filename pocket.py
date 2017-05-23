#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from os import path
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=path.join(model_path, 'fr'),
    lm=path.join(model_path, 'fr.lm.bin'),
    dic=path.join(model_path, 'cmudict-fr.dict')
)

for phrase in speech:
    print(phrase)