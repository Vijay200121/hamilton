import speech_recognition as sr
import os


def callAssistant():
    """it cals the assistant as soon as user says hey jarvis or hello jarvis"""
    check = open(".\\checkopenclose.txt","r")
    data = check.read()
    check.close()
    callassistant = ''
    a = sr.Recognizer()
    if data=="closed":
        with sr.Microphone() as source:
            a.adjust_for_ambient_noise(source)
            a.pause_threshold = 1.5
            print("listenning....", end="\r")
            audioc = a.listen(source)

        try:
            print("Recognizing....\n")
            callassistant = a.recognize_google(audioc, language='en-in')
            
            if "Hamilton" in callassistant:
                os.startfile(".\\myAssistant.pyw")
                closing = open("checkopenclose.txt","w")
                closing.write("opened")
                closing.close()
            elif "quit" in callassistant:
                exit()

        except Exception as e:
            print("sorry i could not understand please try again\n")
            print('-'*140)
    else:
        pass

while (True):
    callAssistant()
