import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import subprocess

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up the microphone 
with sr.Microphone() as microphone:
    # Increase microphone sensitivity
    microphone.energy_threshold = 200

# Set speaking rate
engine.setProperty('rate', 170)

# Set up the Zira voice
voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    """Speaks the given text using the speaker"""
    print(f"Cleopatra: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(prompt_word, timeout=10):
    """Listens for a user command using the microphone"""
    with sr.Microphone() as source:
        # Adjust for ambient noise before each input
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)
    try:
        # Use Google Web Speech API to recognize the command
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        if prompt_word in command.lower():
            return command.lower().replace(prompt_word, "").strip()
        elif "youtube" in command.lower():
            query = command.lower().replace("youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query}"
            speak(f"Okay, I am searching for {query} on YouTube")
            webbrowser.open(url)
        elif "itunes" in command.lower():
            speak("Opening iTunes")
            subprocess.Popen("C:/Program Files/iTunes/iTunes.exe")
        elif "volume up" in command.lower():
            volume_up()
        elif "volume down" in command.lower():
            volume_down()
        elif "play music" in command.lower():
            speak("Playing music")
            subprocess.Popen("C:/Program Files/iTunes/iTunes.exe")
        elif "open spotify" in command.lower():
            speak("Opening Spotify")
            subprocess.Popen("C:/Users/[username]/AppData/Roaming/Spotify/Spotify.exe")
        elif "play playlist" in command.lower():
            query = command.lower().replace("play playlist", "").strip()
            url = f"https://open.spotify.com/search/{query}"
            speak(f"Okay, I am searching for {query} on Spotify")
            webbrowser.open(url)
        elif "play song" in command.lower():
            query = command.lower().replace("play song", "").strip()
            speak(f"Okay, I am searching for {query} on iTunes")
            subprocess.Popen(f"C:/Program Files/iTunes/iTunes.exe {query}")
        else:
            return None
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        speak("I'm sorry, I didn't understand that. Could you please repeat?")
        return None
    except sr.RequestError:
        print("Sorry, I couldn't access the speech recognition service.")
        speak("I'm sorry, I couldn't access the speech recognition service. Please check your internet connection.")
        return None

def volume_up():
    """Increases the master volume by 10%"""
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        current_volume = volume.GetMasterVolume()
        new_volume = min(current_volume + 0.1, 1.0)  # increase by 10%, but not above 100%
        volume.SetMasterVolume(new_volume, None)

def volume_down():
    """Decreases the master volume by 10%"""
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        current_volume = volume.GetMasterVolume()
        new_volume = max(current_volume - 0.1, 0.0)  # decrease by 10%, but not below 0%
        volume.SetMasterVolume(new_volume, None)

# Greet the user
speak("Hello! My name is Cleopatra. How may I assist you today?")

# Listen for the user's commands and respond accordingly
while True:
    command = listen("cleopatra")

    if command is None:
        continue  # continue listening

    elif "search" in command:
        search_query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        try:
            webbrowser.open(url)
            speak(f"Okay, I am searching for {search_query} on the web")
        except Exception as e:
            print(f"Error opening URL: {e}")
            speak("Sorry, there was an error trying to open the search results.")

    elif "time" in command:
        time_now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time_now}")

    elif "hello" in command:
        speak("Hi there!")

    elif "how are you" in command:
        speak("I'm doing well, thank you for asking.")

    elif "what's your name" in command or "who are you" in command:
        speak("My name is Cleopatra, and I'm here to help you with anything you need.")

    elif "itunes" in command.lower():
        speak("Opening iTunes")
        subprocess.Popen("C:/Program Files/iTunes/iTunes.exe")

    elif "volume up" in command.lower():
        volume_up()
        speak("Volume increased")

    elif "volume down" in command.lower():
        volume_down()
        speak("Volume decreased")

    elif "play music" in command.lower():
        speak("Playing music")
        subprocess.Popen("C:/Program Files/iTunes/iTunes.exe")

    elif "open spotify" in command.lower():
        speak("Opening Spotify")
        subprocess.Popen("C:/Users/[username]/AppData/Roaming/Spotify/Spotify.exe")

    elif "play playlist" in command.lower():
        query = command.lower().replace("play playlist", "").strip()
        url = f"https://open.spotify.com/search/{query}"
        speak(f"Okay, I am searching for {query} on Spotify")
        webbrowser.open(url)

    elif "play song" in command.lower():
        query = command.lower().replace("play song", "").strip()
        speak(f"Okay, I am searching for {query} on iTunes")
        subprocess.Popen(f"C:/Program Files/iTunes/iTunes.exe {query}")