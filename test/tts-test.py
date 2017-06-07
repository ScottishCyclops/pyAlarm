from gtts import gTTS

from utils import command


def say_text(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("say.wav")
    command("mplayer say.wav")


def main():
    text = "what the fuck mate"

    print(text)

    print("pico")
    command("pico2wave -w say.wav \"" + text + "\" && mplayer say.wav")
    print("festival")
    command("echo \"" + text + "\" | festival --tts")
    print("espeak")
    command("espeak -ven+f3 -k5 -s150 \"" + text + "\"")
    print("google")
    say_text(text, 'en')


if __name__ == "__main__":
    main()
