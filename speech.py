# modules/speech.py
import pyttsx3

def init_tts(enable_tts=False):
    if enable_tts:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 0.9)
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        return engine
    return None

def speak_text(text, engine=None, enable_tts=False):
    if enable_tts and engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"SKY: {text}")

def listen_to_user(enable_stt=False):
    if not enable_stt:
        return input("You: ")
    # Microphone listening can be added here if needed
    return input("You (type for now): ")
