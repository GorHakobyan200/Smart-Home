import pyaudio
import sys
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import webbrowser
import os
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import wikipedia


os.system("python3 face_rec.py")

servoPIN2 = 22
servoPIN = 27
GPIO.setmode(GPIO.BCM)

GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(servoPIN2,GPIO.OUT)


pwm = GPIO.PWM(servoPIN, 50)
pwm2 = GPIO.PWM(servoPIN2, 50)

pwm.start(0) 
pwm2.start(0) 


model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,channels=1,
            rate=16000, input=True,frames_per_buffer=8000)

stream.start_stream()


def talk(words):
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()
talk("Hi sir,can i help you")

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer["text"]:
                yield answer["text"]


for text in listen():
    print(f"[log] Find: {text}")
    if "hello" in text:
        talk("What you want?")
    elif "bye" in text:
        talk("Bye Mr. Hakobyan")
        os.system("python3 jarvis_vosk.py")
        sys.exit()
    elif "website" in text:
        talk("one minute sir")
        webbrowser.open("https://youtube.com")
    elif "news" in text:
        talk("one minute sir")
        webbrowser.open("https://news.am")
    elif "tree" in text:
        talk("one minute sir")
        os.system("python3 L-System-3.py")
    elif "jarvis" in text:
        talk("Yes sir, I listen you")
    
    elif "name" in text:
        talk("My name is Jarvis")
    elif "about" in text:
        talk("I am Jarvis, the Virtual Voice Assitant created by Gor Hakobyan")
    
    elif "translate" in text:
        b = text
        a = b.split(" ",1)[-1]
        talk("one minute sir")
        webbrowser.open(f"https://translate.google.com/?sl=en&tl=hy&text={a}&op=translate")
    elif "restaurants" in text:
        talk("one minute sir")
        webbrowser.open("https://www.google.com/search?sxsrf=ALeKk00u6dXGvZnMfnMNm2AtLDhMDi3MGw%3A1613503459880&ei=4xssYJqWNcuOlwTTtorYAQ&q=restaurants&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYAjIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzoJCCMQsAMQJxATOgsIABCwAxAHEB4QEzoHCAAQsAMQEzoGCCMQJxATOgQIABATUK8wWOg0YMzaAmgCcAB4AoAByQSIAYkIkgEHMC4zLjUtMZgBAKABAaoBB2d3cy13aXqwAQrIAQrAAQE&sclient=gws-wiz")
    
    elif "find information " in text:
        try:
            a = text
            b = a.split(" ",2)[-1]
            wikipedia.set_lang("en")
            c = wikipedia.summary(b)
            talk("one minute sir")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{b}")
            talk(c)
        except:
            continue

    elif "thank you" in text :
        talk("You are welcome sir")

    elif "one minute" in text:
        talk("Ok,sir")
    elif "power off" in text:
        talk("Ok ser computer shutting down")
        os.system("shutdown /p")
    elif "open" in text:
        pwm.ChangeDutyCycle(10)
        talk("Doors are opened")

    elif "close" in text or "class" in text or "colors" in text:                
        pwm.ChangeDutyCycle(2.5)
        talk("Doors are closed")

    elif "turn on" in text:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(14,GPIO.OUT)
        GPIO.output(14,GPIO.HIGH)
        talk("Lights are turned on")

    elif "turn off" in text:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(14,GPIO.OUT)
        GPIO.output(14,GPIO.LOW)
        talk("Lights are turned off")
    elif "temperature" in text:
        while True:
            dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
            try:
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
                print(f"Temperature is {int(temperature_c)} degrees Celsius , and is {int(temperature_f)} degrees Fahrenheit and air humidity is {humidity}%")
                talk(f"Temperature is {int(temperature_c)} degrees Celsius , and is {int(temperature_f)} degrees Fahrenheit and air humidity is {humidity}%")
                break
            except RuntimeError as error:
                print(error.args[0])
                print(error)
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error
