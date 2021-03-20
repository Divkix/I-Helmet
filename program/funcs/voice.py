import pyttsx3

from .log import logerr, loginfo

# Pyttsx config for voice feedback
engine = pyttsx3.init()
engine.setProperty("rate", 140)

# Funtion to Log Assistant Dialogs and make Assistant Speak
def speak(text):
    loginfo(f"Assistant: {text}\n")
    engine.say(text)
    engine.runAndWait()


# Speak Error message
def speak_err(text):
    logerr(f"Assistant: {text}\n")
    engine.say(f"Error: {text}")
    engine.runAndWait()
