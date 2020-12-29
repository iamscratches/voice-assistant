from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import pyttsx3
import pytz
import subprocess
import webbrowser
import bs4 as bs  
import urllib.request
from GoogleNews import GoogleNews


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]

def google_news():
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
    
    while(True):
        news = googlenews.result()
        for i in range(0,len(news)):            
            print("title = " + news[i]['title'])
            print("media = " + news[i]['media'])
            print("date = " + news[i]['date'])
            print("link = " + news[i]['link'])
            speak(news[i]['title'])
            speak(news[i]['desc'])        
            print("\n\n")
        speak("would you like to hear more??")
        text = get_audio()    
        if("no" in text):
            speak("ok duely noted")
            break
        googlenews.clear()
        googlenews.getpage(2)


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day,service):
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

def speak(text):
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 125)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male

    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    print('listening...')
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            return "ERROR"
    return said.lower()

def get_date(text):
    text = text
    print(text)
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    print(text.split())
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
            print('month found')
        elif word in DAYS:
            day_of_week = DAYS.index(word)
            print('day found')
        elif word.isdigit():
            day = int(word)
            print('day found 2')
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                        print('day found 3')
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
            if text.count("next") >= 1:
                dif +=7
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None
    return datetime.date(month = month, day = day, year = year)
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe",file_name])
def filterDate(text):
    datentime = str(datetime.datetime.now()).split()    
    date = datentime[0]
    time = datentime[1]
    time = time
    date = list(date.split("-"))
    ampm = "am"
    extension = "th"
    if date[2][-1] == "1":
        extension = "st"
    elif date[2][-1] == "2":
        extension = "nd"
    elif date[2][-1] == "3":
        extension = "rd"
    print(date)
    filtered_date = "" + date[2] + extension + " " + MONTHS[int(date[1]) - 1] + " "

    time = time.split(":")
    if int(time[0]) > 12:
        ampm = "pm"
        time[0] = str(int(time[0]) % 12)
    filtered_time =  "" + time[0] + ":" + time[1] + " " + ampm
    if "time" in text:
        return filtered_time
    else:
        return filtered_date
    
SERVICE = authenticate_google()
CALENDER_STRS = ["what do i have","do i have plans","am i busy", "plans"]
NOTE_STRS = ["make a note","write this down","take a note","write down","note"]
NAMES = ["scratches", "sketches","50","crutches","traces","rajesh","catches"]
TIME = ["time","date"]
SEARCH_ITEMS = ["search", "what is", "what are"]
DEFINE_TERMS = ["define"]
SEARCH_LOCATION = ["locate", "find a location"]
SEARCH_YOUTUBE = ["video"]
SEARCH_NEWS = ["news"]
start_time = time.time()
while(True):
    text = get_audio()
    if(text == "ERROR"):
        print("outside ERROR")
        print("waiting for {}".format(int(time.time() - start_time)))
        continue    
    if(set(text.split())&set(NAMES)):        
        speak("i am listening...")
        start_time = time.time()
        
        while(time.time() - start_time < 30):
            text = get_audio()
            print("waiting for {}".format(int(time.time() - start_time)))            
            if(text == "ERROR"):
                print("Inside ERROR")
                print("waiting for {}".format(int(time.time() - start_time)))
                continue 
            
            start_time = time.time()
            
#CHECKED DEFINE_TERMS
            if(set(text.split()) & set(DEFINE_TERMS)):
                print("define")
                text = text.replace("define ", "")
                text = text.replace(" ", "_")
                search_term = 'https://en.wikipedia.org/wiki/' + text
                print(search_term)
                raw_html = urllib.request.urlopen(search_term)  
                raw_html = raw_html.read()
                article_html = bs.BeautifulSoup(raw_html, 'lxml')
                article_paragraphs = article_html.find_all('p')
                speak(article_paragraphs[0].text)
                continue
            
#CHECKED SEARCH_YOUTUBE
            if(set(text.split()) & set(SEARCH_YOUTUBE)):
                url = f"https://www.youtube.com/results?search_query={text}"
                webbrowser.get().open(url)
                speak("here is a video!! hope this helps!!")
                continue

#CHECKED SEARCH_LOCATION            
            if(set(text.split()) & set(SEARCH_LOCATION)):
                speak("what would you like me to locate!!")
                search = get_audio()
                if(search == "ERROR"):
                    print("Inside Inside ERROR")
                    print("waiting for {}".format(int(time.time() - start_time)))
                    speak("sorry i did'nt hear u respond, so i'm assuming you found what you were looking for!!")
                    continue 
                url = "https://google.nl/maps/place/" + search + "/&amp;"
                webbrowser.get().open(url)
                speak("here is the location")
                continue

#CHECKED SEARCH_ITEMS        
            if(set(text.split()) & set(SEARCH_ITEMS)):   
                text = text.replace("search","")
                url = "https://google.com/search?q=" + text
                webbrowser.get().open(url)
                speak("here is what i found")
                continue

#CHECKED CALENDER_STRS                
            if(set(text.split()) & set(CALENDER_STRS)): 
                date = get_date(text)
                print(date)
                if date:
                    speak('The date you asked for is ' + str(date))
                    get_events(date,SERVICE)
                else:
                    speak("i can't hear you please try again!!")
                    break
                continue

#CHECKED NOTE_STRS
            if(set(text.split()) & set(NOTE_STRS)): 
                speak("what would you like me to write down?")
                note_text = get_audio()
                note(note_text)
                speak("I've made a note of that.")
                continue

#CHECKED TIME                         
            if(set(text.split())&set(TIME)):
                print(str(datetime.datetime.now()))
                speak(filterDate(text))
                continue

#CHECKED SEARCH_NEWS
            if(set(text.split())&set(SEARCH_NEWS)):
                google_news()
                continue

            if(set(text.split())&set(NAMES)):                
                speak("i am listening...")
                start_time = time.time()
                continue

            if("bye" in text.split() or "tata" in text.split()):   
                break
            
            speak("sorry, i didn't quiet understand u can u ask again please!!")
            
            
    elif "hello" in text:
        speak("hello, how are u?")
    elif "your name" in text:
        speak("My name is Scratches")
    if "bye" in text or "tata" in text:
        speak("ok! bye bye!, nice to meet you")
        break










    

