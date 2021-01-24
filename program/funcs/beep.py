import winsound

# Define Beep to make sound
def beep(duration=500):
    # Set Duration To 500 ms == 0.5 second
    frequency = 2500  # Set Frequency To 2500 Hertz
    winsound.Beep(frequency, duration)