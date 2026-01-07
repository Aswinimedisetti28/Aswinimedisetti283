import speech_recognition as sr

def record_voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... please speak your mood.")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand your voice."
        except sr.RequestError:
            return "Could not request results. Please check internet connection."
