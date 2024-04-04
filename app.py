from flask import Flask
import pyttsx3
app = Flask(__name__)

def speak(response):
    engine = pyttsx3.init()
    voice = engine.getProperty("voices")
    engine.setProperty("voice", voice[1].id)
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 0.9)
    engine.say(response)
    engine.runAndWait()
    
@app.route('/')
def hello_world():
    speak("Hello Thanos Congratulations Your api is finally hosted . Now give us a Big treat.")
    return "Hii Thanos"