import datetime,wikipedia,webbrowser,os,random,requests
import Annex, wolframalpha
from ttkthemes import themed_tk
import tkinter as tk
from tkinter import scrolledtext
from functools import partial
import pyttsx3
import speech_recognition as sr
import sys
import re
import smtplib
import youtube_dl
import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from time import strftime
from tkinter import *
from PIL import ImageTk,Image
import threading

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        SR.speak("Good Morning!")
    elif hour>=12 and hour<18:
        SR.speak("Good Afternoon!")
    else:
        SR.speak("Good Evening!")
    SR.speak("I am Aidva. Please tell me how may I help you")

def on_click():
    def myCmd():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say something...')
            SR.updating_ST('Say Something...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            cmd = r.recognize_google(audio).lower()
            SR.updating_ST('You said: ' + cmd + '\n')
        except sr.UnknownValueError:
            SR.updating_ST('....')
            cmd = myCmd()
        return cmd

    def assistant(cmd):
        if 'open reddit' in cmd:
            reg_ex = re.search('open reddit (.*)', cmd)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            SR.speak('The Reddit content has been opened for you Sir.')

        elif 'shutdown' in cmd or 'exit' in cmd or 'stop' in cmd:
            SR.speak('Bye bye Sir. Have a nice day')
            sys.exit()
        elif 'open' in cmd:
            reg_ex = re.search('open (.+)', cmd)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain + '.com'
                webbrowser.open(url)
                speak('The website you have requested has been opened for you Sir.')
            else:
                pass
        elif 'hello' in cmd:
            day_time = int(strftime('%H'))
            if day_time < 12:
                SR.speak('Hello Sir. Good morning')
            elif 12 <= day_time < 18:
                SR.speak('Hello Sir. Good afternoon')
            else:
                SR.speak('Hello Sir. Good evening')

        elif 'help' in cmd:
            SR.updating_ST("""
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Tell a joke/another joke : Says a random dad joke.
            4. Current weather in {cityname} : Tells you the current condition and temperture
            5. Greetings
            6. play me a video : Plays song in your VLC media player
            7. change wallpaper : Change desktop wallpaper
            8. news for today : reads top news of today
            9. time : Current system time
            10. top stories from google news (RSS feeds)
            1. tell me about xyz : tells you about xyz
            """)
            speak("You can use these commands and I'll help you out:")
        elif 'news for today' in cmd:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    print(news.title.text.encode('utf-8'))
                    speak(news.title.text.encode('utf-8'))
            except Exception as e:
                    print(e)
        elif "weather" in cmd:
                api_key="8ef61edcf1c576d65d836254e11ea420"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                SR.speak("what's the city name")
                city_name=myCmd()
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    SR.updating_ST('---Temperature in kelvin unit---')
                    SR.speak('Temperature is :' + str(current_temperature))
                    SR.updating_ST('---Humidity---')
                    SR.speak('humidity is ' + str(current_humidiy))
                    SR.updating_ST('---Description---')
                    SR.speak('description  ' + str(weather_description))
        elif 'time' in cmd:
            import datetime
            now = datetime.datetime.now()
            SR.updating_ST("%d:%d"%(now.hour, now.minute))
            speak('Current time is %d hours %d minutes' % (now.hour, now.minute))
        elif 'game' in cmd:
            moves=["rock", "paper", "scissor"]
            cmove=random.choice(moves)
            speak("Choose among rock paper or scissor")
            pmove=myCmd()
            SR.speak("The computer chose " + cmove)
            SR.speak("You choose " + pmove)
            if pmove==cmove:
                SR.speak("the match is draw")
            elif pmove== "rock" and cmove== "scissor":
                SR.speak("you wins")
            elif pmove== "rock" and cmove== "paper":
                SR.speak("Computer wins")
            elif pmove== "paper" and cmove== "rock":
                SR.speak("you wins")
            elif pmove== "paper" and cmove== "scissor":
                SR.speak("Computer wins")
            elif pmove== "scissor" and cmove== "paper":
                SR.speak("you wins")
            elif pmove== "scissor" and cmove== "rock":
                SR.speak("Computer wins")
        elif 'toss' in cmd or 'flip' in cmd or 'coin' in cmd:
            moves=["head", "tails"]   
            cmove=random.choice(moves)
            print(cmove)
            speak("The computer choose " + cmove)
        elif 'email' in cmd:
            speak('Who is the recipient?')
            recipient = myCmd()
            if 'david' in recipient:
                speak('What should I say to him?')
                content = myCmd()
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('xyz@gmail.com', '*************')
                mail.sendmail('abc.com', 'amdp.hauhan@gmail.com', content)
                mail.close()
                speak('Email has been sent successfuly. You can check your inbox.')
            else:
                speak('I don\'t know what you mean!')
        elif 'who are you' in cmd or 'what is your name' in cmd:
            speak('I am your personal voice assistant Aidva')
        elif 'ask' in cmd:
            SR.speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=myCmd()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            SR.speak(answer)
        if 'wikipedia' in cmd:
                speak('Searching Wikipedia...')
                cmd = cmd.replace("wikipedia", "")
                results = wikipedia.summary(cmd, sentences=2)
                speak("According to Wikipedia")
                SR.speak(results)
    wishMe()
    speak('I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')
    while True:
        assistant(myCmd())
def gen(n):
    for i in range(n):
        yield i
class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        on_click()
def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()
if __name__=="__main__":
        #tkinter code
        root=themed_tk.ThemedTk()
        root.geometry("{}x{}+{}+{}".format(745,360,int(root.winfo_screenwidth()/2 - 745/2),int(root.winfo_screenheight()/2 - 360/2)))
        root.resizable(0,0)
        root.title("Aidva")
        root.iconbitmap('./Desktop/Project/icon.ico')
        root.configure(bg='#2c4557')
        scrollable_text=scrolledtext.ScrolledText(root,state='disabled',height=15,width=87,relief='sunken',bd=5,wrap=tk.WORD,bg='#add8e6',fg='#800000')
        scrollable_text.place(x=10,y=10)
        mic_img=Image.open("./Desktop/Project/Mic.png")
        mic_img=mic_img.resize((55,55), Image.Resampling.LANCZOS)
        mic_img=ImageTk.PhotoImage(mic_img)
        Speak_label=tk.Label(root,text="SPEAK:",fg="#FFD700",font='"Times New Roman" 12 ',borderwidth=0,bg='#2c4557')
        Speak_label.place(x=250,y=300)
        """Setting up objects"""
        SR=Annex.SpeakRecog(scrollable_text)  
        Listen_Button=tk.Button(root,image=mic_img,borderwidth=0,activebackground='#2c4557',bg='#2c4557',command=Launching_thread)
        Listen_Button.place(x=330,y=280)
        myMenu=tk.Menu(root)
        m1=tk.Menu(myMenu,tearoff=0)
        myMenu.add_cascade(label="Help",menu=m1)
        stng_win=Annex.SettingWindow()
        myMenu.add_cascade(label="Settings",command=partial(stng_win.settingWindow,root))
        root.config(menu=myMenu)
        root.mainloop()