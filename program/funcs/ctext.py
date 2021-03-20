# For Colorured Text when the program starts
import sys

from colorama import init

from .log import logerr, loginfo

init(strip=not sys.stdout.isatty())
from pyfiglet import figlet_format
from termcolor import cprint


def ctext(text, font="slant", color="green"):
    cprint(figlet_format(text, font=font), color)
    loginfo(f"Printing {text} color text, {font} font with color color")
