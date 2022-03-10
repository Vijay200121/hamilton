"""this program is a simple assiatant which can help in day to day usage of pc like opening of applications, play music, ask time, search on google, youtube, send email, cuerrentlu the functions and applocations are limited.
to give command to open application on pc kindli check in the program first which applications are supported from line number 134.
to play music update the directory path at line no 115 of this code"""

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import pymysql.cursors
from playsound import playsound
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import multiprocessing


def database_connect():
    """connect to databse to extract values"""
    try:
        con = pymysql.connect(host='localhost',
                          user='USER',
                          password='yourPass',
                          database='assistant',
                          cursorclass=pymysql.cursors.DictCursor)
        bind = con.cursor()
        print("successfully connected to databse!")
    except Exception as e:
        print("could not connect to database")
        speak("could not connect to database, please try later")
    return bind

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishuser():
    """this function wishesthe user as soon as the assistent is started.
    this greets the user with good morning, afternoon or evening based on current time.
    and ask if need nay help from assistent."""

    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good morning")
        speak("Good Morning!")
    elif 12 <= hour < 17:
        print("good afternoon")
        speak("Good Afternoon!")
    else:
        print("good evening")
        speak("Good Evening!")

    speak("I am Hamilton, how can i help ?")

def callAssistant():
    """it cals the assistant as soon as user says hey jarvis or hello jarvis"""
    calljarvis = ''
    a = sr.Recognizer()
    with sr.Microphone() as source:
        a.adjust_for_ambient_noise(source)
        a.pause_threshold = 1.5
        audioc = a.listen(source)

    try:
        calljarvis = a.recognize_google(audioc, language='en-in')
    except Exception as e:
        print("sorry i could not understand please try again\n")
        print('-'*140)

    return calljarvis

def takeCommand():
    """it takes the command from user and recognise it to perform the task."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        playsound("listening sound.mp3")
        print("Listening....", end="\r")
        r.pause_threshold = 1.5
        audio = r.listen(source)
        
    try:
        print("Recognizing....\n")
        playsound("recognizing sound.mp3")
        query = r.recognize_google(audio, language='en-in')
        print(f"{f'you :- {query}' : >125}\n")
    except Exception as e:
        # print(e)
        print('-'*140)
        speak("Sorry, I can't understand, please try again, ")
        return "None"
    return query

def extractMail(name):
    bind = database_connect()
    command = bind.execute('select mail_id from mail_ids where name =(%s)',(name))
    if command == False:
        print(f"cannot fetch mail id of {name}\n")
        print('-'*140)
        speak("Something went wrong, please try again..")
    else:
        data = bind.fetchone()
    return data

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("*******@gmail.com", "******")
    server.sendmail("*******@gmail.com", to, content)

class FindSongs():
    """finds and returns the desired songs from the directory"""

    music_dir = ''#path to songs folder
    songs = os.listdir(music_dir)
    total_songs = len(songs)
    song_no = 0
    found = False

    def __init__(self, songname):
        self.songname = songname

    def getDetails(self):
        for i in range(0, self.total_songs):
            self.songs[i] = self.songs[i].lower()
            if self.songname in self.songs[i]:
                self.song_no = i
                self.found=True
                break

        #return self.song_no

class FindMovie():
    """finds and returns the desired songs from the directory"""

    movie_dir = ''#path to movies folder
    movies = os.listdir(movie_dir)
    total_movies = len(movies)
    movie_no = 0
    found = False

    def __init__(self, moviename):
        self.moviename = moviename

    def getDetails(self):
        for i in range(0, self.total_movies):
            self.movies[i] = self.movies[i].lower()
            if self.moviename in self.movies[i]:
                self.movie_no = i
                self.found=True
                break


def openApp(query):
    """contains the paths to all the applications which can be opened by jarvis"""

    global appPath
    try:
        if "whatsapp" in query:
            appPath = "C:\\Users\\vijay gaike\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
        elif "vs code" in query:
            appPath = "C:\\Users\\vijay gaike\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        elif "blender" in query:
            appPath = "C:\\Program Files\\Blender Foundation\\Blender 3.0\\blender-launcher.exe"
        elif "chrome" in query:
            appPath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        elif "xamp" in query:
            appPath = "C:\\xampp\\xampp-control.exe"
        elif "powerdirector" in query:
            appPath = "C:\\Program Files\\CyberLink\\PowerDirector20\\PDR.exe"
        elif "android studio" in query:
            appPath = "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe"
        elif "codeblocks" in query:
            appPath = "C:\\Program Files\\CodeBlocks\\codeblocks.exe"
        elif "oracle" in query:
            appPath = "C:\\oraclexe\\app\\oracle\\product\\10.2.0\\server\\Database_homepage.url"
        elif "sql command line" in query:
            appPath = "C:\\oraclexe\\app\\oracle\\product\\10.2.0\\server\\BIN\\sqlplus.exe //nolog"
        elif "r studio" in query:
            appPath = "C:\\Program Files\\RStudio\\bin\\rstudio.exe"
        elif "calculator" in query:
            appPath = "C:\\Windows\\System32\\calc.exe"
        elif "cmd" in query:
            appPath = "C:\\Windows\\System32\\cmd.exe"
        elif "command prompt" in query:
            appPath = "C:\\Windows\\System32\\cmd.exe"
        elif "control panel" in query:
            appPath = "C:\\Windows\\System32\\control.exe"
        elif "notepad" in query:
            appPath = "C:\\Windows\\System32\\notepad.exe"
        else:
            speak("sorry, cannot find the requested application on this system")
            appPath = ""

    except Exception as e:
        pass
    return appPath


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


root = tk.Tk()
def gui():
    root.geometry("200x100+1055+575")
    root.resizable(False,False)
    root.overrideredirect(True)
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load("searchgif.gif")
    root.mainloop()

webbrowser.register('chrome', None,webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))

def commands():
    """user commands execution"""
    query = takeCommand().lower()

    # logic for execution of tasks based on query
    if "wikipedia" in query:
        speak("Searching wikipedia....")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        print('-'*140)
        speak("According to wikipedia")
        speak(results)

    # elif "open youtube" in query:
    #     webbrowser.get('chrome').open("youtube.com")
    #     print('-'*140)
    # elif "open google" in query:
    #     webbrowser.get('chrome').open("google.com")
    #     print('-'*140)

    elif "play music" in query:
        print("Which song would you like to play ?\n")
        speak("Which song would you like to play ?")
        songname = takeCommand()
        songinfo = FindSongs(songname.lower())
        songinfo.getDetails()
        if songinfo.found == True:
            speak("playing requested song..!")
            print(f"\nplaying song number :- {songinfo.song_no}\nsong name :- {songinfo.songs[songinfo.song_no]}\n")
            os.startfile(os.path.join(songinfo.music_dir, songinfo.songs[songinfo.song_no]))
            print('-'*140)
        else:
            print("requested song not found..!\n")
            print('-'*140)
            speak("requested song not found!")
    
    elif "play movie" in query:
        print("Which movie would you like to play ?\n")
        speak("Which movie would you like to play ?")
        moviename = takeCommand()
        movieinfo = FindMovie(moviename.lower())
        movieinfo.getDetails()
        if movieinfo.found == True:
            print(f"\nplaying song number :- {movieinfo.movie_no}\nmovie name :- {movieinfo.movies[movieinfo.movie_no]}\n")
            os.startfile(os.path.join(movieinfo.movie_dir, movieinfo.movies[movieinfo.movie_no]))
            print('-'*140)
        else:
            print("requested movie not found..!\n")
            print('-'*140)
            speak("requested movie not found!")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        print(f"Time :- {strTime}\n")
        print('-'*140)
        speak(f"Its {strTime}")

    elif "open" in query:
        codePath = openApp(query)
        os.startfile(codePath)
        print('-'*140)

    elif "send email" in query:
        try:
            speak("Whome to send..?")
            name = takeCommand()
            name = name.lower()
            mailid = extractMail(name)
            print(f'name :- {name}')
            print(f'mail id :- {mailid}')
            speak("what do you want to send ?")
            content = takeCommand()
            to = mailid
            print(f'content :- {content}')
            speak(f"are you sure to send this mail to {name}")
            confirmation = takeCommand()
            if "yes" in confirmation:
                sendEmail(to, content)
                print("mail sent!\n")
                print('-'*140)
                speak("your mail has been sent...!")
            else:
                try:
                    speak('do you want to save this as draft?')
                    draftConfirm = takeCommand()
                    if "yes" in draftConfirm:
                        draft = open("draft.txt", "a")
                        draft.write("\n",'-'*20,"\n\n",content)
                        draft.close()
                        print("message saved as draft..!\n")
                        print('-'*140)
                        speak("message saved as draft..!")
                    else:
                        speak("message not saved as draft..!")
                        content = ""
                except Exception as e:
                    speak("could not save message as draft")
        
        except Exception as e:
            print("could not send mail, please try again.\n")
            print('-'*140)
            speak("could not send mail, please try again.")

    elif "search" in query:
        tosearch = query.replace("search", "")
        if "on youtube" in tosearch:
            tosearch = tosearch.replace("on youtube", "")
            webbrowser.get('chrome').open_new_tab('http://www.youtube.com/search?btnG=1&q=%s' % tosearch)
            print('-'*140)

        elif "on google" in tosearch:
            tosearch = tosearch.replace("on google", "")
            webbrowser.get('chrome').open_new_tab('http://www.google.com/search?btnG=1&q=%s' % tosearch)
            print('-'*140)
    elif "quit" in query:
        speak("thank you, you can call me anytime!")
        exit()


p1 = multiprocessing.Process(target=commands)
p2 = multiprocessing.Process(target=gui)

if __name__ == "__main__":
    p2.start()
    wishuser()
    p1.start()
    p1.join()
    p2.kill()
    p1.kill()
    closefile = open("checkopenclose.txt","w")
    closefile.write("closed")
    closefile.close()
