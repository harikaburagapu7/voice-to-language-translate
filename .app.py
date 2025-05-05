
import datetime
import os
import time
import tkinter as tk
import webbrowser
from tkinter import messagebox, simpledialog

import pygame
import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice rate
engine.setProperty('rate', 150)

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Function to speak and print Jersiva's response
def speak(text):
    jersiva_text = f"Jersiva: {text}"
    print(jersiva_text)  # Display Jersiva's response in the console
    engine.say(text)
    engine.runAndWait()

# Function to listen for commands and print user's command
def listen_command():
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)  # Listen for the audio

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio_data)  # Recognize speech using Google Speech Recognition
        print("You said:", text)
        return text.lower()

    except sr.UnknownValueError:
        print("Sorry, I could not understand your audio.")
        return ""  # Return an empty string if speech is not understood

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""  # Return an empty string if there's an issue with the service

# Function to get weather information
def get_weather():
    api_key = "your_openweathermap_api_key"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "your_city_name"  # Replace with your city name
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") != 200:
        error_message = data.get("message", "Error retrieving weather data")
        return f"Failed to get weather data: {error_message}"

    main = data["main"]
    temperature = main["temp"]
    pressure = main["pressure"]
    humidity = main["humidity"]
    weather_desc = data["weather"][0]["description"]
    weather_report = (f"Temperature: {temperature - 273.15:.2f}°C\n"
                      f"Pressure: {pressure} hPa\n"
                      f"Humidity: {humidity}%\n"
                      f"Description: {weather_desc}")
    return weather_report

# Function to process commands
def process_command(command):
    if "open chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("http://www.google.com")
    elif "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open my youtube channel" in command:
        speak("Opening your youtube channel")
        webbrowser.open(
            "https://l.instagram.com/?u=https%3A%2F%2Fwww.youtube.com%2Fchannel%2FUCGBIJ4Lg-1jXLUgxb34R34A&e=AT10Z0YoyLwvfYeD8DVqKP04tEMoICG8TZnTifMTj0ljeEeFo0szN57SSQUL3TuCoiZzS0mRfE0kR1iYyzpjjRPl5M49JcFqaE0xegm5rIFC9Z7Bpa_exrI")
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "open edge" in command:
        speak("Opening Microsoft Edge")
        os.system("start msedge")
    elif "open settings" in command:
        speak("Opening Settings")
        os.system("start ms-settings:")
    elif "open vs code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")
    elif "open devc++" in command:
        speak("Opening Dev-C++")
        os.system("start devcpp")
    elif "open control panel" in command:
        speak("Opening Control Panel")
        os.system("control")
    elif "weather" in command:
        speak("Getting weather information")
        weather_info = get_weather()
        speak(weather_info)
    elif "tell me a joke" in command:
        speak("Here's a joke for you")
        joke = pyjokes.get_joke()
        speak(joke)
    elif "how are you" in command:
        speak("I'm doing well, thanks for asking! How about you?")
    elif "describe yourself" in command:
        speak(
            "I'm your virtual assistant, designed to help you with various tasks like setting reminders, managing your schedule, and providing information.")
    elif "i am fine" in command:
        speak("That's great to hear! Is there anything I can assist you with?")
    elif "set a timer" in command:
        speak("For how many seconds?")
        duration = listen_command()
        if duration.isdigit():
            speak(f"Setting a timer for {duration} seconds")
            time.sleep(int(duration))
            speak("Time's up!")
        else:
            speak("Invalid duration")
    elif "set an alarm" in command:
        speak("Please tell me the time to set the alarm. For example, say 'set alarm at 6:30 AM'.")
        alarm_time = listen_command()
        if alarm_time:
            try:
                alarm_hour, alarm_minute = map(int, alarm_time.split(" ")[2].split(":"))
                period = alarm_time.split(" ")[3].lower()
                if period == "pm" and alarm_hour != 12:
                    alarm_hour += 12
                elif period == "am" and alarm_hour == 12:
                    alarm_hour = 0
                while True:
                    current_time = datetime.datetime.now()
                    if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
                        speak("Wake up! It's time to start your day!")
                        break
            except ValueError:
                speak("Sorry, I couldn't set the alarm. Please try again.")

# Function to translate text
def translate(text, dest_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Sorry, I couldn't translate that."

# Function to convert text to speech and play the sound
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        output_file = "output.mp3"
        tts.save(output_file)

        # Play the generated audio
        sound = pygame.mixer.Sound(output_file)
        sound.play()

        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)  # Adjust playback speed

        os.remove(output_file)  # Remove the file after playback
    except Exception as e:
        print(f"Text-to-speech error: {e}")

# Function to get languages through tkinter dialog
def get_languages():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    source = simpledialog.askstring("Input", "Please enter source language (e.g., en, fr):")
    dest = simpledialog.askstring("Input", "Please enter destination language (e.g., en, es):")

    if not source or not dest:
        messagebox.showerror("Error", "Source and destination languages are required!")
        return None, None

    return source, dest

# Main loop
def main():
    speak("Hello, Jersiva is ready. Please enter your source and destination languages.")

    source_lang, dest_lang = get_languages()
    if not source_lang or not dest_lang:
        return

    messagebox.showinfo("Voice Translator", "Press OK and then speak something to translate.")

    while True:
        input_text = listen_command()
        if input_text:
            translated_text = translate(input_text, dest_lang)
            if translated_text:
                print(f"Translated Text: {translated_text}")
                text_to_speech(translated_text, dest_lang)
                print("Would you like to translate another phrase or change the languages?")
                response = listen_command()
                if "another" in response or "change" in response:
                    if "change" in response:
                        source_lang, dest_lang = get_languages()
                        if not source_lang or not dest_lang:
                            return
                    continue  # Go back to listening for new input
                else:
                    speak("Goodbye!")
                    break  # Exit the loop if the user doesn't want to continue
            else:
                print("Failed to translate the text.")
        else:
            print("No input received.")

            action = messagebox.askquestion(
                "Next Action",
                "Do you want to translate another phrase, change the language, or stop?",
                icon='question',
                type=messagebox.YESNOCANCEL,
                default=messagebox.YES
            )

            if action == 'cancel':
                break
            elif action == 'no':
                source_lang, dest_lang = get_languages()
                if not source_lang or not dest_lang:
                    return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program...")
        sys.exit(0)
