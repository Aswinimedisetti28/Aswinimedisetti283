import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

print("Recognizing...")
print(r.recognize_google(audio, language="en-IN"))
