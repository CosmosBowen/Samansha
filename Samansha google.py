# voices[].id
#     0:ZH-CN_HUIHUI
#     1:EN-US_ZIRA

import time
from hashlib import new
import queue
import re
from types import NoneType
import webbrowser
import pyttsx3
import speech_recognition as sr

import requests
# import bs4
import lxml
from bs4 import BeautifulSoup
engine = pyttsx3.init()
greeting = "Hi, I'm Samansha. Nice to meet you. Please tell me what you wanna know."
isContinue = False
isBreak = False
isEnter = False


def Speak(text):
    voices = engine.getProperty('voices')
    voice = voices[1].id
    engine.setProperty('voice', voice)
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()


def WhatISaidIs():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("I'm recognizing...")
        speech = recognizer.recognize_google(audio, language='en-us').lower()
        Speak(f"You just said: {speech}")
    except Exception as e:
        speech = "none"
        Speak("I didn't get it.")
    return speech


def callback(recognizer, audio):
    try:
        notes = recognizer.recognize_google(audio, language='en-us').lower()
        print(notes)
        if "next" in notes:
            global isContinue
            isContinue = True
        elif "stop" in notes:
            global isBreak
            isBreak = True
        elif "click" in notes:
            global isEnter
            isEnter = True
        # if notes == "next":
        #     global isContinue
        #     isContinue = True
        # elif notes == "stop":
        #     global isBreak
        #     isBreak = True
        # elif notes == "enter":
        #     global isEnter
        #     isEnter = True
    except sr.UnknownValueError:
        print("Google Speech Recog3nition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
    # try:
    #     speech = recognizer.recognize_google(audio, language='zh-cn')
    # except Exception as e:
    #     speech = "none"
    # if speech == "下一条":
    #     print("下一条")
    # elif speech == "进入这条":
    #     print("进入这条")
    # elif speech == "停止":
    #     print("停止")


# ------------
Speak(greeting)
# word = WhatISaidIs().lower()
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    print("I'm listening...")
    r.pause_threshold = 0.5
    r.adjust_for_ambient_noise(source)
    audio = r.listen(m)

# ------------
try:
    print("I'm recognizing...")
    word = r.recognize_google(audio, language='en-us')
    Speak(f"You just said:{word}")
except Exception as e:
    word = "none"
    Speak("I didn't get it.")
print(word)

# ------------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

html = requests.get(
    "https://www.google.com/search?q="+word, headers=headers)
html.raise_for_status()
soup = BeautifulSoup(html.text, "lxml")
results = soup.select(".tF2Cxc")
# ------------
Speak("I just found"+str(len(results)) +
      "pieces of information here, they are as followed...")

# recognizer = sr.Recognizer()
# microphone = sr.Microphone()
# with microphone as source:
#     recognizer.pause_threshold = 0.5
#     recognizer.adjust_for_ambient_noise(source, duration=1)
#     stop_listening = recognizer.listen_in_background(microphone, callback)
#     stop_listening(wait_for_stop=False)

stop_listening = r.listen_in_background(m, callback)

# ::::::::::
# for i in range(50):
#     if isContinue:
#         continue
#     if isBreak:
#         break
#     print(i)
#     time.sleep(10)
# stop_listening(wait_for_stop=True)
# print("done")

# ::::::::::
# while True:
#     # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
#     time.sleep(0.1)

for result in results:
    isContinue = False
    isEnter = False
    title = result.select_one(".DKV0Md").text
    link = result.select_one(".yuRUbf a")["href"]
    spans = result.select(".lEBKkf span")
    if len(spans) > 1:
        date = spans[1].text
        snippet = spans[len(spans)-1].text
    else:
        date = ""
        snippet = result.select_one(".lEBKkf span")
        # snippet = result.select_one(".lEBKkf span")
        if snippet is NoneType or snippet is None:
            snippet = ""
        else:
            snippet = snippet.text

    # displayed_link = result.select_one(".lEBKkf span").

    showText = title+"\n"+date + \
        ("" if date == "" else "\n")+snippet + \
        ("" if snippet == "" else "\n")+link+"\n"
    print(showText)

    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        isEnter = False
    Speak("Title is "+title)
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        isEnter = False
    if (snippet == ""):
        Speak("No snippet.")
    else:
        Speak("Snippet is "+snippet)
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        isEnter = False
    if (date == ""):
        Speak("No issue date.")
    else:
        Speak("It's issued on "+date)
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        # print("点开了该链接:"+link+"...DONE!")
        isEnter = False

    # print(f"{title}\n{link}\n{date}\n{snippet}\n")

stop_listening(wait_for_stop=False)
print("done")

# if __name__ == '__main__':
#     Speak(greeting)
#     WhatISaidIs()
