import json
import os

from .log import logerr, loginfo

# Get Exact location of the commands.json file
curr_dir = os.getcwd()
flst = curr_dir.split("\\")

cmDir = ""
for i in flst:
    cmDir += i + "/"
cmDir += "commands.json"

# Load data from commands.json file
with open(cmDir) as f:
    dict_data = json.loads(f.read())


def load_all_cmd_stuff():
    command_list = load_commands()
    commands_help = load_help()
    return command_list, commands_help


# Load Commands List
def load_commands():
    commands = {}
    for cmd in list(dict_data.keys()):
        lst = []
        for item in dict_data[cmd]["commands"]:
            lst.append(item.lower())
        commands[cmd] = lst
        del lst
    loginfo("Loaded commands list!")
    return commands


# Load Commands for help
def load_help():
    commands_help = {}
    for cmd in list(dict_data.keys()):
        helptxt = dict_data[cmd]["help_text"]
        commands_help[cmd] = helptxt
        del helptxt
    loginfo("Loaded commands help!")
    return commands_help
