# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:28:03 2020

@author: subhankar
"""
from __future__ import print_function
import datetime
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# import time
import pytz
import subprocess
import webbrowser
import bs4 as bs  
import urllib.request
from GoogleNews import GoogleNews

from apis.IOFeatures import speak, get_audio, speakThread

__SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
__MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
__DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
__DAY_EXTENSIONS = ["nd", "rd", "th", "st"]


# GOOGLE CALENDER AUTHENTICATION

def __authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('credentials\\token.pickle'):
        with open('credentials\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials\\credentials.json', __SCOPES)
            creds = flow.run_local_server(port=0)
        with open('credentials\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service
  
__SERVICE = __authenticate_google()


# ASK FOR DEFINITION OF A PARTICULAR TERM FROM THE BOT
def define(text):
    text = text.replace("define ", "")
    text = text.replace("explain ", "")
    text = text.replace("explain the term ", "")
    text = text.replace("what is the meaning of ", "")
    text = text.replace("what is ", "")
    text = text.replace("what are ", "")
    text = text.replace("who is ", "")
    text = text.replace("where is ", "")
    text = text.replace(" ", "_")
    search_term = 'https://en.wikipedia.org/wiki/' + text
    print(search_term)
    raw_html = urllib.request.urlopen(search_term)  
    raw_html = raw_html.read()
    article_html = bs.BeautifulSoup(raw_html, 'lxml')
    article_paragraphs = article_html.find_all('p')
    info = article_paragraphs[1].text 
    while(len(info) < 200):
        info = info + article_paragraphs[2].text 
    info = info.replace("[1]","")
    info = info.replace("[2]","")
    info = info.replace("[3]","")
    info = info.replace("[4]","")
    info = info.replace("[5]","")
    info = info.replace("[6]","")
    
    print(article_paragraphs[0].text + "\n" + article_paragraphs[1].text + "\n" + article_paragraphs[2].text)
    speak(info,200)


# SEARCH THE YOUTUBE FOR A PARTICULAR VIDEO
def playVideo(text):
    url = f"https://www.youtube.com/results?search_query={text}"
    webbrowser.get().open(url)

# SEARCH THE LOCATION OF A PARTICULAR PLACE
def findLocation():    
    search = get_audio()
    if(search == "ERROR"):
        speak("sorry i did not hear u respond, so i'm assuming you found what you were looking for!!")
        return
    url = "https://google.nl/maps/place/" + search + "/&amp;"
    webbrowser.get().open(url)
    speak("here is the location")

# PERFORM A GOOGLE SEARCH ASKED BY THE BOT
def googleSearch(text):
    text = text.replace("can you make a google search on ","")
    text = text.replace("google on ","")
    text = text.replace("google for ","")
    text = text.replace("google ","")
    text = text.replace("search for the keyword ","")
    text = text.replace("search for ","")
    text = text.replace("search ","")
    
    url = "https://google.com/search?q=" + text
    webbrowser.get().open(url)

# CHECK GOOGLE CALENDER FOR SCHEDULE OF A PARTICULAR DAY

def __get_events(day,service):
    # Call the calender API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(),singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day. ")
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12 :
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + "at" + start_time)



def __get_date(text):
    text = text
    print(text)
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    elif text.count("tomorrow") > 0:
        return today + datetime.timedelta(1)

    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    print(text.split())
    for word in text.split():
        if word in __MONTHS:
            month = __MONTHS.index(word) + 1
            # print('month found')
        elif word in __DAYS:
            day_of_week = __DAYS.index(word)
            # print('day found')
        elif word.isdigit():
            day = int(word)
            # print('day found 2')
        else:
            for ext in __DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                        # print('day found 3')
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif< 0:
            dif += 7
            print("hello")
        if text.count("next") > 0:
            dif +=7
            print("here")
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None
    return datetime.date(month = month, day = day, year = year)

def calenderCheck(text):
    date = __get_date(text)
    speak('The date you asked for is ' + str(date))
    __get_events(date,__SERVICE)
    
# MAKE A NOTE FOR A PARTICULAR EVENT TO BE REMEMBERED

def noteMaker(text):
    date = datetime.datetime.now()
    speak("Would you like to give a name to your note??")
    
    if("yes" in (get_audio()).split()):
    # if("yes" in "no"):
        speakThread("Please say the name for your note...")
        rename = get_audio()
        file_name = rename.replace(" ","_") + ".txt"
    else:
        speak("ok sir!! no problem i'll save it myself with a date and time stamp so that you may know when it's created")
        file_name = str(date).replace(":","-") + "-note.txt"
    file_path = "notes\\" + file_name
    with open(file_path,"w") as f:
        f.write(text)
    speak("Your note has been successfully saved under the name of" + file_name)
    subprocess.Popen(["notepad.exe",file_path])

# RETURN THE DATE AND TIME OF THE MOMENT WHEN ASKED

def dateTime(text):
    datentime = str(datetime.datetime.now()).split()    
    date = datentime[0]
    time = datentime[1]
    date = list(date.split("-"))
    ampm = "am"
    extension = "th"
    if date[2][-1] == "1":
        extension = "st"
    elif date[2][-1] == "2":
        extension = "nd"
    elif date[2][-1] == "3":
        extension = "rd"
    
    filtered_date = "" + date[2] + extension + " " + __MONTHS[int(date[1]) - 1] + " "

    time = time.split(":")
    if int(time[0]) > 12:
        ampm = "pm"
        time[0] = str(int(time[0]) % 12)
    filtered_time =  "" + time[0] + ":" + time[1] + " " + ampm
    if "time" in text:
        # speak(filtered_time)
        return filtered_time
    else:
        return filtered_date + " " + filtered_time

# SEARCH DAILY NEWS FOR A PARTICUALR TOPIC

def findNews():
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    speak("do you have a specific topic in mind??")
    text = get_audio()
    while(text == "ERROR" or "ok go back" in text):
        if("ok go back" in text):
            return
        speak("sorry let's try again")
        speak("do you have a specific topic in mind??")
        text = get_audio() 
        
        continue
    if text == "no":
        googlenews.search('world')
    else:
        googlenews.search(text)    
    
    page = 2
    while(True):
        news = googlenews.result()
        for i in range(0,len(news)):            
            print("title = " + news[i]['title'])
            print("media = " + news[i]['media'])
            print("date = " + news[i]['date'])
            print("link = " + news[i]['link'])
            speak(news[i]['title'],150)
            speak(news[i]['desc'],210)        
            print("\n\n")
        speak("would you like to hear more??")
        text = get_audio() 
        if("no" in text and "ERROR" in text):
            speak("ok duely noted")
            break
        googlenews.clear()
        googlenews.getpage(page)
        page = page + 1
