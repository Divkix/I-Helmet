import sounddevice as sd
import requests
import speech_recognition as sr
import time

# Local modules
from .log import start_logging, logerr, loginfo
from .ctext import ctext
from .clear import clear
from .pingloc import ping_location
from .voice import speak, speak_err
from .loadcmds import load_all_cmd_stuff


def start_system_dialog():
    clear()
    ctext("Starting System...")
    clear()
    ctext("Started System!")


# Initialize System
def initialize():
    start_logging()  # Start logging

    try:
        loginfo("Loading Audio Devices...")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            loginfo(
                f'Microphone with name "{index}" found for `Microphone(device_index={name})`'
            )
        loginfo(sd.query_devices())
        loginfo("Loaded Devices!")
    except Exception as ef:
        logerr("Could not load devices!")
        logerr(f"{ef}")
    time.sleep(2)  # Sleep for stability
    (
        command_list,
        commands_help,
    ) = load_all_cmd_stuff()  # Load commands_list and commands_help
    time.sleep(1)  # Sleep for stability
    start_system_dialog()
    ip_request = requests.get("https://get.geojs.io/v1/ip.json")
    Start_ip = ip_request.json()["ip"]
    ip, Lat_loc, Long_loc = ping_location(Start_ip)
    loginfo("Obtaining IP Address...")
    loginfo(f"Obtained IP Address: {Start_ip}")
    speak("Welcome to I Helmet Assistant.\nSay Help to check commands and help.")
    return ip, Lat_loc, Long_loc, command_list, commands_help