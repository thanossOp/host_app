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

@app.route('/', methods=['GET'])
def call_script():
    speak("Hello Thanos! How are you? Congratulations! Your application is hosted successfully. Now give us a treat.")
    return "Welcome Thanos on titan"

if __name__ == "__main__":
    app.run(debug=True)
