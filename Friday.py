import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import pyjokes

engine = pyttsx3.init('sapi5')  #sapi is microsoft speech api to convert text to speech
voices = engine.getProperty('voices')  #This fetches voices
engine.setProperty('voice', voices[1].id) #we are selecting first voice out of voice list

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning!")
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        print("Good Afternoon!")
        speak("Good Afternoon!")

    else:
        print("Good Evening!")
        speak("Good Evening!")
    
    print("I am Jarvis. How may I assist you today?")
    speak("I am Jarvis. How may I assist you today")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Could not Recognize that please try again...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('uselessacco80@gmail.com', 'Password')
    server.sendmail('uselessacco80@gmail.com', to, content)
    server.close()

def getWeather(city):
    api_key = "74fec6dc40410a6d462bb4437160d7f5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    
    #Print the raw JSON response for debugging purposes
    #print(json.dumps(data, indent=4))
    
    if data.get("cod") != 200:  # OpenWeatherMap uses "cod" for status codes
        error_message = data.get("message", "")
        speak(f"City not found or there was an error with the request. Error message: {error_message}")
        return

    main = data.get("main")
    if main is not None:
        temperature = main.get("temp")
        weather_description = data["weather"][0].get("description")
        if temperature is not None and weather_description is not None:
            temperature_celsius = temperature - 273.15
            print(f"The temperature in {city} is {temperature_celsius:.2f} degrees Celsius with {weather_description}.")
            speak(f"The temperature in {city} is {temperature_celsius:.2f} degrees Celsius with {weather_description}.")
        else:
            speak("Could not retrieve temperature or weather description.")
    else:
        speak("Could not retrieve weather data.")

def getNews():
    api_key = "00002fee3a994cb38157edf1dee92194"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    news = response.json()
    
    # Print the raw JSON response for debugging purposes
    #print(json.dumps(news, indent=4))
    
    if news.get("status") != "ok":
        error_message = news.get("message", "Error fetching news")
        speak(f"Could not fetch news. Error message: {error_message}")
        return

    articles = news.get("articles")
    if articles is not None and len(articles) > 0:  # Check if articles list is not empty
        top_article = articles[0]  # Get the first article (top headline)
        headline = top_article.get("title")
        if headline:
            print(f"Top Headline: {headline}")
            speak(f"Top Headline: {headline}")
        else:
            print("No headline found.")
            speak("No headline found.")
    else:
        print("No articles found.")
        speak("No articles found.")


def tellJoke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def tellQuote():
    quotes = [
        "The best way to get started is to quit talking and begin doing.",
        "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.",
        "Don’t let yesterday take up too much of today.",
        "You learn more from failure than from success. Don’t let it stop you. Failure builds character."
    ]
    import random
    quote = random.choice(quotes)
    print(quote)
    speak(quote)

def remember(content):
    with open('memory.txt', 'w') as f:
        f.write(content)
    speak("I will remember that.")

def recall():
    with open('memory.txt', 'r') as f:
        content = f.read()
    if content:
        speak(f"You asked me to remember: {content}")
    else:
        speak("I don't remember anything")

def setReminder(time, message):
    speak(f"Setting a reminder for {time} with message: {message}")
    with open('reminders.txt', 'a') as f:
        f.write(f"{time}: {message}\n")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open chat gpt' in query:
            webbrowser.open("chatgpt.com")    

        elif 'play music' in query:
            music_dir = 'P:\\ntg\\EDITS\\Audios'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = ""E:\\HTML\\demo.html""
            os.startfile(codePath)

        elif 'send an email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "prajwalshettar43@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")

        elif 'who are you' in query:
            print("Hello I am Jarvis made by prajwal and team created for Anveshana")
            speak("Hello I am Jarvis made by prajwal and team created for Anveshana")
            print("You can ask me to 'search google for' or tell quote or joke or 'set a remainder' or 'weather in' or 'open bec website' or 'play music' or 'play a game' or 'news'")
            speak("You can ask me to. search google for or. tell quote or joke or. set a remainder or. weather in or. open bec website or. play music or. play a game or. news")

        elif 'how are you' in query:
            print("Hello I am Jarvis made by prajwal and team created for Anveshana")
            speak("Hello I am Jarvis made by prajwal and team created for Anveshana")
            print("You can ask me to 'search google for' or tell quote or joke or 'set a remainder' or 'weather in' or 'open bec website' or 'play music' or 'play a game' or 'news'")
            speak("You can ask me to. search google for or. tell quote or joke or. set a remainder or. weather in or. open bec website or. play music or. play a game or. news")

        elif 'weather in' in query:
            city = query.split("in")[-1].strip()
            getWeather(city)

        elif 'news' in query:
            getNews()

        elif 'joke' in query:
            tellJoke()

        elif 'quote' in query:
            tellQuote()

        elif 'remember' in query:
            content = query.replace("remember", "").strip()
            remember(content)
            content = query.replace("remember", "").strip()
            remember(content)

        elif 'remind' in query:
            recall()

        elif 'set a reminder' in query:
            try:
                parts = query.split("for")
                time = parts[1].strip().split("to")[0].strip()
                message = parts[1].strip().split("to")[1].strip()
                setReminder(time, message)
            except IndexError:
                print("Sorry, I couldn't understand the time and message for the reminder.")
                speak("Sorry, I couldn't understand the time and message for the reminder.")
        
        elif 'open bec website' in query:
            webbrowser.open("becbgk.edu")

        elif 'search google for' in query:
            search_query = query.replace('search google for', '').strip()
            google_search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(google_search_url)

       # elif 'add ' in query:

        elif 'game' in query:
            webbrowser.open("slowroads.io")

        elif 'exit' in query:
            print("Thank you!")
            speak("Thank you!")
            exit()