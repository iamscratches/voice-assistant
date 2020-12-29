# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 15:45:51 2020

@author: subhankar
"""












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










    

