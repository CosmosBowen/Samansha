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
greeting = "你好，我叫Samansha，很高兴与你交流，请您说出想要搜索的内容"
isContinue = False
isBreak = False
isEnter = False


def Speak(text):
    voices = engine.getProperty('voices')
    voice = voices[0].id
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()


def WhatISaidIs():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("我正在听...")
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("正在识别语音...")
        speech = recognizer.recognize_google(audio, language='zh-cn')
        Speak(f"你刚刚说：{speech}")
    except Exception as e:
        speech = "none"
        Speak("我没有听清楚。")
    return speech


def callback(recognizer, audio):
    try:
        notes = recognizer.recognize_google(audio, language='zh-cn')
        print(notes)
        if notes == "跳过":
            global isContinue
            isContinue = True
        elif notes == "停止":
            global isBreak
            isBreak = True
        elif notes == "进入":
            global isEnter
            isEnter = True
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
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
    print("我正在听...")
    r.pause_threshold = 0.5
    r.adjust_for_ambient_noise(source)
    audio = r.listen(m)

# ------------
try:
    print("正在识别语音...")
    word = r.recognize_google(audio, language='zh-cn')
    Speak(f"你刚刚说：{word}")
except Exception as e:
    word = "none"
    Speak("我没有听清楚。")
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
Speak("为您找到"+str(len(results))+"条信息，如下...")

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
    Speak("标题:"+title)
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        isEnter = False
    if (snippet == ""):
        Speak("无摘要。")
    else:
        Speak("摘要:"+snippet)
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        isEnter = False
    if (date == ""):
        Speak("无发布时间。")
    else:
        Speak(date+"发布。")
    if isContinue:
        continue
    if isBreak:
        break
    if isEnter:
        webbrowser.open(link)
        # print("点开了该链接:"+link+"...DONE!")
        isEnter = False

    # print(f"{title}\n{link}\n{date}\n{snippet}\n")

stop_listening(wait_for_stop=True)
print("done")

# if __name__ == '__main__':
#     Speak(greeting)
#     WhatISaidIs()
