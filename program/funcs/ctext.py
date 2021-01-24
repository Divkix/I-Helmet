from .log import logerr, loginfo

# For Colorured Text when the program starts
import sys
from colorama import init

init(strip=not sys.stdout.isatty())
from termcolor import cprint
from pyfiglet import figlet_format


def ctext(text, font="slant", color="green"):
    cprint(figlet_format(text, font=font), color)
    loginfo(f"Printing {text} color text, {font} font with color color")