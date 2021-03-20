import os


# Clear output in console
def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")
