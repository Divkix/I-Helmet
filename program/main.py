# Import necessary modules
import os
import sys
import time

# For catching error!
import traceback
import webbrowser
from datetime import datetime

import speech_recognition as sr
from funcs.beep import beep
from funcs.ctext import ctext
from funcs.initialize import initialize
from funcs.log import logerr, loginfo

# Import Realtime detection
from funcs.realtimedetection import objectdetection, realtime_detection
from funcs.voice import speak, speak_err

# Variables
wakeup = start_nav = start_help = False
Start_ip, Lat_loc, Long_loc = None, None, None
command_list = {}
commands_help = {}
classes, CLASSES_Mobile_DNN = None, None


# Make sure script keeps running in background.
def start_I_Helmet():
    with open("yolo_files/coco.names") as f:
        classes = f.read().strip().split("\n")

    with open("mobile_net_models/classes.txt") as f:
        CLASSES_Mobile_DNN = f.read().strip().split("\n")

    # Set global vars to keep them in memory!
    global Start_ip, Lat_loc, Long_loc, command_list, commands_help
    # Initialize Assistant
    Start_ip, Lat_loc, Long_loc, command_list, commands_help = initialize()

    while True:
        # Start Speech Recognization
        r = sr.Recognizer()
        with sr.Microphone() as mic:
            speak("Please say a command after the Beep.")
            """beep()
            r.adjust_for_ambient_noise(mic)
            audio = r.listen(mic, timeout=5)  # Listen for 5 seconds"""

        try:
            # stt = r.recognize_google(audio)
            command_spoken = input("Enter Command: ")  # stt.lower()
            loginfo(f"User: {command_spoken}")

            # Start Commands
            if command_spoken in command_list["Time"]:
                now = datetime.now()
                h_ctime = ctime = now.strftime("%H")
                m_ctime = ctime = now.strftime("%M")
                ctime = f"The current time is {h_ctime} {m_ctime}"
                speak(ctime)

            elif command_spoken in command_list["Status Check"]:
                # TO-DO: Self Analysis of Script
                speak("All systems working Normally!")

            elif command_spoken in command_list["Shutdown"]:
                speak("Turning off system...")
                ctext("Shutting down...")
                quit(1)

            elif command_spoken in command_list["Realtime Detection"]:
                speak("Starting Realtime Detection")
                beep()
                # Stat Realtime detetion using function
                realtime_detection(classes)

            elif command_spoken.split(" ", 1)[0] in (command_list["Find"][0]):
                count = 0
                wakeup = True
                while count < 5 and wakeup == True:
                    beep(1000)
                    try:
                        object_find = command_spoken.split(" ", 1)[1]
                        if object_find in CLASSES_Mobile_DNN:
                            speak(f"Searching for {object_find}")
                            found = False
                            found, deg, direction = objectdetection(
                                object_find,
                                CLASSES_Mobile_DNN,
                            )
                            if found == True:
                                speak("Object found!")
                                direction = "Ahead"
                                if dir == -1:
                                    direction = "Left"
                                elif dir == 1:
                                    direction = "Right"
                                st = (
                                    str(object_find)
                                    + " found at "
                                    + str(int(deg))
                                    + " Degree "
                                    + str(direction)
                                )
                                speak(st)
                                wakeup = False
                            else:
                                speak("Could not find object in the frame.")
                                count += 1
                        else:
                            speak("Object not found in Pre Defined Classes!")
                            break
                    except Exception as err:
                        time.sleep(1)
                        count += 1
                        speak_err(err)

            elif command_list["Navigation"][0] in command_spoken:
                start_nav = True
                location = command_spoken.split(" ", 2)[2]
                if location and start_nav:
                    speak(f"Taking you to {location}")
                    params = {
                        "saddr": f"{Lat_loc},{Long_loc}",
                        "daddr": f"{location}",
                        "nav": "1",
                    }
                    speak("Launching Google Maps...")
                    webbrowser.open(f"https://www.google.com/maps/place/{location}")
                    webbrowser.open(f"http://maps.google.com/maps?{params}")
                    start_nav = False
                    time.sleep(5)

            elif command_spoken.split(" ", 1)[0] == "help":
                start_help = True
                if (len(command_spoken.split(" ")) == 1) and (
                    command_spoken.split(" ")[0] == "help"
                ):
                    speak(
                        f"The following modules are loaded: {list(commands_help.keys())}. Speak help followed by module name to know more about an specific module.",
                    )
                elif len(command_spoken.split(" ")) >= 2:
                    help_statement = command_spoken.split(" ", 1)[1]
                    if start_help and help_statement:
                        if help_statement == "navigation":
                            speak(commands_help["Navigation"])
                        elif help_statement in command_list["Find"]:
                            speak(commands_help["Find"])
                        elif help_statement in command_list["Realtime Detection"]:
                            speak(commands_help["Realtime Detection"])
                        elif help_statement in command_list["Status Check"]:
                            speak(commands_help["Status Check"])
                        elif help_statement in command_list["Shutdown"]:
                            speak(commands_help["Shutdown"])
                        elif help_statement in command_list["Time"]:
                            speak(commands_help["Time"])
                        else:
                            speak("Speak a proper module of command name!")
                        start_help = False

            else:
                speak("Command not Found!")

        except sr.UnknownValueError:
            pass

        except sr.WaitTimeoutError:
            pass

        except Exception as ef:
            speak_err(ef)
            print(traceback.format_exc())
            print(sys.exc_info()[-1].tb_lineno)


if __name__ == "__main__":
    start_I_Helmet()
