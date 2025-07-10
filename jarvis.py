import speech_recognition as sr
import pyttsx3
import sys
import webbrowser
import os
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

# os.system("python3.7 face_rec.py")

def talk(words):
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()
talk("Hello World")


servoPIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization



def command():
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)

    try:
        task = r.recognize_google(audio).lower()
        print(task)
    except:
        talk("I don't listen please say again")
        task = command()
    return task

def working(task):
    if "hello" in task:
        talk("Hello Gor Hakobyan,can i help you?")
        print("Hello")
    elif "bye" in task:
        talk("bye Gor Hakobyan")
        sys.exit()
    elif "website" in task:
        talk("one minute sir")
        webbrowser.open("https://youtube.com")
    elif "news" in task:
        talk("one minute sir")
        webbrowser.open("https://news.am")
    elif "draw" in task:
        talk("one minute sir")
        os.system("L-System-3.py")


    elif "name" in task:
        talk("My name is Jarvis")
    elif "about" in task:
        os.system("JARVIS.mp4")
    elif "translate" in task:
        b = task
        a = b.split(" ",1)[-1]
        talk("one minute sir")
        webbrowser.open(f"https://translate.google.com/?sl=en&tl=hy&text={a}&op=translate")
    elif "resturants" in task:
        talk("one minute sir")
        webbrowser.open("https://www.google.com/search?sxsrf=ALeKk00u6dXGvZnMfnMNm2AtLDhMDi3MGw%3A1613503459880&ei=4xssYJqWNcuOlwTTtorYAQ&q=restaurants&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYAjIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzoJCCMQsAMQJxATOgsIABCwAxAHEB4QEzoHCAAQsAMQEzoGCCMQJxATOgQIABATUK8wWOg0YMzaAmgCcAB4AoAByQSIAYkIkgEHMC4zLjUtMZgBAKABAaoBB2d3cy13aXqwAQrIAQrAAQE&sclient=gws-wiz")

    elif "thank you" in task :
        talk("You are welcome sir")

    elif "one minute" in task:
        talk("Ok,sir")
    elif "turn off computer" in task:
        talk("Ok ser computer shutting down")
        os.system("shutdown /p")
    elif "open doors" in task:
        p.ChangeDutyCycle(7.5)
    elif "close doors" in task:                
        p.ChangeDutyCycle(2.5)

    elif "turn on light" in task:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(14,GPIO.OUT)
        GPIO.output(14,GPIO.HIGH)
    elif "turn off light" in task:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(14,GPIO.OUT)
        GPIO.output(14,GPIO.LOW)
    elif "temperature" in task:
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

while True:
    working(command())