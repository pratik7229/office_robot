import pyttsx3
import webbrowser
from googlesearch import *
import InputOutput
import functions


engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def commandsViaVoice():
    while True:
            query = InputOutput.takeCommand().lower()
            if (query == 'stop' or query == 'exit'):
                break
            else:
                AllQuerise(query)

def AllQuerise(query):  #query mahnje apn input deleli string eg. age, whats the date

            if 'open youtube' in query:
                webbrowser.open("youtube.com")
                InputOutput.speak("Opening Youtube.com...")

            elif 'open google' in query:
                webbrowser.open("google.com")
                InputOutput.speak("Opening Google.com...")