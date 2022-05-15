# Libraries
import pyttsx3
import speech_recognition as sr
from googlesearch import *
import sys
import time
import multiprocessing




engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[11].id)


def speak(audio):
    """
    This function is used to make the system speak
    """
    
    engine.say(audio)
    engine.runAndWait()

def PrintStr(strslow, ts):
    for l in strslow:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(ts)


def speakPrint(spstr):
    p1 = multiprocessing.Process(target=PrintStr, args=(spstr, 0.031))
    p2 = multiprocessing.Process(target=speak, args=(spstr,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

def takeCommand():
    '''
    It takes microphone input from user and returns string output!
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


