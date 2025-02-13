
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
import pyttsx3

app = Flask(__name__)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Error connecting to Google API"

def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def text_to_speech(text, lang):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_lang = data.get('language')
    translated_text = translate_text(text, target_lang)
    return jsonify({'translated_text': translated_text})

if __name__ == "__main__":
    app.run(debug=True)
