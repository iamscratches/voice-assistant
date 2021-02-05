# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 13:17:09 2020

@author: subhankar
"""


from apis.chatbot1 import chat
from apis.IOFeatures import get_audio, speak, speakThread
from apis.APIFeatures import define, playVideo, findLocation, googleSearch, calenderCheck, noteMaker, dateTime, findNews
import time

start_time = time.time()
while(True):
    text = get_audio()
    if(text == "ERROR"):
        # print("outside ERROR")
        # print("waiting for {}".format(int(time.time() - start_time)))
        continue 
    tag, response = chat(text)
    if(tag == "wakeup"):        
        speakThread(response)
        start_time = time.time()
        while(time.time() - start_time < 15):
            text = get_audio()
            # print("waiting for {}".format(int(time.time() - start_time)))            
            if(text == "ERROR"):
                # print("Inside ERROR")
                # print("waiting for {}".format(int(time.time() - start_time)))
                continue 
            
            
            tag, response = chat(text)
            if(tag == "greeting" or tag == "age" or tag == "name"):
                speak(response)
            elif(tag == "define"):# problem
                speak(response)
                define(text)
            elif(tag == "youtube"):
                playVideo(text)
                speak(response)
            elif(tag == "location"):
                speak(response)
                findLocation()
            elif(tag == "google search"):
                googleSearch(text)
                speak(response)
            elif(tag == "calender"):
                speak(response)
                calenderCheck(text)
            elif(tag == "note"):
                speak(response)
                information = get_audio()
                noteMaker(information)
            elif(tag == "date n time"):
                speak(response, 200)
                speak(dateTime(text),120)
            elif(tag == "news"):# stop button, needs training
                speak(response)
                findNews()
            elif(tag == "wakeup"):        
                speak(response)            
            elif(tag == "none"):
                speakThread(response)
            elif(tag == "goodbye"):
                speak(response)
                break
            start_time = time.time()
    elif (tag == "greeting"):
        speak(response)
    elif "bye" in text or "tata" in text:
        speak("ok! bye bye!, nice to meet you")
        break
                
                
