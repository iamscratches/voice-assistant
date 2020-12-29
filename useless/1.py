from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang = "en")
    filename = "voice1.mp3"
    tts.save(filename)
    playsound.playsound(filename)
speak("hello suvnkr")

print("hello")

