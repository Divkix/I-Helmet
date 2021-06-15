import os


# Clear output in console
def clear():
    _ = os.system("cls") if os.name == "nt" else os.system("clear")
