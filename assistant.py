import csv
import os
import smtplib
import webbrowser
from datetime import datetime

import pyaudio
import pyttsx3  # python text-to-speech engine 3
import speech_recognition as sr
import wikipedia

emails = {
    'amber': '************@gmail.com',
    'my other mail' : '********@gmail.com',
    'papa': '***********@gmail.com'
}
c_list = []

# init function to get an engine instance for the speech synthesis
engine = pyttsx3.init('sapi5')      #microsoft's Speech API 5

voices = engine.getProperty('voices')          #getting a list of voices from Microsoft SAPI5

                                                        # for voice in voices:
                                                        #     print(voice)

                                                # print(voices[0].id)    || My computer has only one voice i.e., Anna
engine.setProperty('voice' ,voices[0].id)        #setting audio of Anna as engine property as 'voice'

def speak(audio):
    # say method on the engine that passing input text to be spoken
    engine.say(audio)
    # run and wait method, it processes the voice commands.
    engine.runAndWait()

def wishMe():
    '''
        Will make the program to wish the user as per the time
    '''
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    if int(current_time[0:2]) >= 5 and int(current_time[0:2]) <= 11:
        return f'Good Morning'
    elif int(current_time[0:2]) >= 12 and int(current_time[0:2]) <= 17:
        return f'Good Afternoon'
    elif int(current_time[0:2]) >= 18 and int(current_time[0:2]) <= 21:
        return f'Good Evening'
    elif int(current_time[0:2]) >= 22 and int(current_time[0:2]) <= 4:
        return f'Good Night'

def intro():
    '''
        Let Anna introduce herself
    '''
    speak("My name is Anna, How may I help you?")

def listening():
    '''
        Will listen to the user and convert the audio to text
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  
        audio = r.listen(source)  

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  
            print(f"User said: {query.capitalize()}")  
        except Exception:
            print("Couldn't recognize. Please say that again.")
            return "None"
    return query

def sendEmail():
    server = smtplib.SMTP('64.233.184.108')   #server = smtplib.SMTP('64.233.184.108') IP address of smtp.gmail.com, to bypass DNS resolution
    server.ehlo()
    server.starttls()
    with open('details.csv') as file:
        content = csv.DictReader(file)
        for rows in content:
            server.login(rows['id'], rows['password'])
            print("Whom do you want to send this email?")
            speak("Whom do you want to send this email?")
            to = listening().lower()
            print("What do you want to send?")
            speak("What do you want to send?")
            content = listening().lower()
            server.sendmail(rows['id'], emails[to], content)
            server.close()
            speak("The email has been sent successfully")
    
if __name__ =="__main__":
    wish1 = wishMe()
    speak(wish1)
    intro()
    while True:
        query = listening().lower()
        if 'wikipedia' in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open facebook' in query:
            webbrowser.open("facebook.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'quit' in query or 'exit' in query:
            exit()
        elif 'what' in query and 'time' in query:
            current__time = datetime.now()
            speak(current__time.strftime("%H:%M:%S"))
            print(current__time.strftime("%H:%M:%S"))
        elif 'what' in query and 'date' in query:
            today = datetime.now()
            speak(today.strftime("%D"))
            print(today.strftime("%D"))
        elif 'what' in query and 'your name' in query:
            speak("My name is Anna.")
            print("My name is Anna.")
        elif 'send email' in query or 'send an email' in query:
            sendEmail()
        elif 'open code' in query:
            os.startfile('C:\\Users\\Lenovo\\Desktop\\Python\\Visual Code\\Code - Insiders.exe')