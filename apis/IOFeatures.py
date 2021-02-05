# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:29:54 2020

@author: subhankar
"""
import speech_recognition as sr
import pyttsx3
import threading

def speakThread(text, rate = 150, volume = 1.0):
    t1 = threading.Thread(target= __startSpeech, args= (text, rate, volume))
    t1.setName("speech")
    t1.start()

def speak(text, rate = 150, volume = 1.0):
    __startSpeech(text, rate, volume)
def __startSpeech(text, rate, volume):
    engine = pyttsx3.init() # object creation

    """ RATE"""
    # rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', rate)     # setting up new voice rate

    """VOLUME"""
    # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',volume)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male
    # print(voices)
    
    print("Scratches : " + text)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    print('listening...')
    # said = input("You : ")
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print("You : " + said)
        except Exception as e:
            print("Exception: " + str(e))
            return "ERROR"
    return said.lower()

# speak("hey there i am scratches it's nice to meet you. May i know your name if u don't mind me asking??",210,0.5)


