#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from gtts import gTTS
import os
import subprocess

def execute_unix(inputcommand):
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
   return output

def say_text(text,lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("say.wav")
    os.system("mplayer say.wav")

text = "yolo"

print(text)

print("pico")
execute_unix("pico2wave -w say.wav \""+text+"\" && mplayer say.wav")
print("festival")
execute_unix("echo \""+text+"\" | festival --tts")
print("espeak")
execute_unix("espeak -ven+f3 -k5 -s150 \""+text+"\"")
print("google")
say_text(text,'en')