import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import pyttsx3  # For text-to-speech
from langdetect import detect
from googletrans import Translator

recognizer = sr.Recognizer()

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 120) 
tts_engine.setProperty('volume', 0.9) 

translator = Translator()

root = tk.Tk()
root.title("Speech Recognition & Translation")
root.geometry("500x650")

speech_text = tk.StringVar()
speech_label = tk.Label(root, text="Recognized Speech:", font=("Helvetica", 14))
speech_label.pack(pady=10)
speech_display = tk.Label(root, textvariable=speech_text, font=("Helvetica", 12), wraplength=400)
speech_display.pack(pady=5)

translated_text = tk.StringVar()
translated_label = tk.Label(root, text="Translated Text:", font=("Helvetica", 14))
translated_label.pack(pady=10)
translated_display = tk.Label(root, textvariable=translated_text, font=("Helvetica", 12), wraplength=400)
translated_display.pack(pady=5)

text_to_speak_label = tk.Label(root, text="Enter Text to Speak:", font=("Helvetica", 14))
text_to_speak_label.pack(pady=10)
text_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
text_entry.pack(pady=5)

def listen_for_speech():
    with sr.Microphone() as source:
        speech_text.set("Listening...")
        root.update() 
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            speech_text.set(f"You said: {text}")
            
            detected_lang = detect(text)
            if detected_lang != 'en':
       
                translation = translator.translate(text, src=detected_lang, dest='en')
                translated_text.set(f"Translated to English: {translation.text}")
            else:
                translated_text.set("Detected language is English; no translation needed.")
        except sr.UnknownValueError:
            speech_text.set("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            speech_text.set(f"Error with Google Speech Recognition: {e}")

def speak_text():
    text = text_entry.get()
    if text:
        tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        messagebox.showwarning("Input Error", "Please enter some text to speak.")

def translate_and_speak_text():
    text = text_entry.get()
    if text:
        detected_lang = detect(text)
        if detected_lang != 'en':
            translation = translator.translate(text, src=detected_lang, dest='en')
            translated_text.set(f"Translated to English: {translation.text}")
            tts_engine.say(translation.text)
        else:
            translated_text.set("Entered text is already in English.")
            tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        messagebox.showwarning("Input Error", "Please enter some text to translate and speak.")

def speak_translated_text():
    text = translated_text.get()
    if text and "Translated to English:" in text:
        tts_engine.say(text.replace("Translated to English: ", ""))  # Remove label prefix
        tts_engine.runAndWait()
    elif text:
        tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        messagebox.showwarning("Translation Error", "No translated text available to speak.")

listen_button = tk.Button(root, text="Start Listening", command=listen_for_speech, font=("Helvetica", 14))
listen_button.pack(pady=20)
speak_button = tk.Button(root, text="Speak Text", command=speak_text, font=("Helvetica", 14))
speak_button.pack(pady=10)
speak_translated_button = tk.Button(root, text="Speak Translated Text", command=speak_translated_text, font=("Helvetica", 14))
speak_translated_button.pack(pady=10)
translate_and_speak_button = tk.Button(root, text="Translate & Speak Entered Text", command=translate_and_speak_text, font=("Helvetica", 14))
translate_and_speak_button.pack(pady=10)

root.mainloop()
