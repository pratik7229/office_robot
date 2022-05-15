# Libraries
from __future__ import print_function
import pyttsx3
import datetime
import requests
import InputOutput

# setting up the voice and engine required for the voice output
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[11].id)



def checkInternetConnection():
    """
    This function is used to check internet connection
    
    """

    url = "http://www.google.com"
    timeout = 5
    # InputOutput.speak("connecting to the servers...")
    try:
        request = requests.get(url, timeout=timeout)
        # InputOutput.speakPrint("connected to the servers sucessfully")
        print("connected to the servers sucessfully")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        InputOutput.PrintStr("Fail to connect to the servers.", 0.005)
        InputOutput.speak("Fail to connect to the servers.")
        return False


def wishMe(name, mode):
    """
    This function whishes the user according to the time with their name
    
    """
    InputOutput.speak(name)
    # InputOutput.speak("How may I help you\n")
    # if mode == 1:
    #     hour = int(datetime.datetime.now().hour)
    #     # if hour >= 0 and hour < 12:
    #     #     InputOutput.speak( "Good Morning"+str(name))
    #     # elif hour >= 12 and hour < 18:
    #     #     InputOutput.speak("Good Afternoon" +str(name))
    #     # else:
    #     #     InputOutput.speak("Good Evening"+str(name))
    #     InputOutput.speak("How may I help you\n")
    # elif mode == 4:
    #     hour = int(datetime.datetime.now().hour)
    #     if hour >= 0 and hour < 12:
    #         InputOutput.speak("Good Morning" + str(name))
    #     elif hour >= 12 and hour < 18:
    #         InputOutput.speak("Good Afternoon" + str(name))
    #     else:
    #         InputOutput.speak("Good Evening" + str(name))
    #     InputOutput.speak("I have a document for you\n")
    # elif mode == 3:
    #     InputOutput.speak("Thankyou for Confirmation\n")
