# Smart-Home

The main files for this project are `face_rec.py` and `jarvis_vos.py`. The concept involves controlling the sensors of a smart home using a Raspberry Pi, utilizing voice commands and a security system with face recognition.

I participated in several hackathons and exhibitions, including DigiTec, and this project also served as my final work in college.

The program begins with face recognition. If my face is recognized, it activates the voice assistant. If an unauthorized person is detected, the system issues a warning, saves an image of the individual, and sends me a notification.

With this program, you can inquire about temperature and humidity using the DHT11 sensor, open or close doors, and turn lights on or off. Additionally, you can ask for information, and the assistant will provide responses.

You also need to install the language pack vosk named "vosk-small-en-0.15". This library is good because you can use it without an internet connection.
