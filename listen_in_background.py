import imp


import time
import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    print(recognizer.recognize_google(audio, language='zh-cn'))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)
    # audio = r.listen(source)
    # speech = r.recognize_google(audio, language='zh-cn')
    # print("刚刚说了"+speech)

stop_listening = r.listen_in_background(m, callback)
print("listening...")

for _ in range(50):
    print("hhhhhh")
    time.sleep(0.1)

# # calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=True)
# print("stop listening.")
