from gpiozero import Button
from signal import pause

# Function called when the sensor is touched
def touched():
    # Print a message indicating the sensor is touched
    print("Touched!")

# Function called when the sensor is not touched
def not_touched():
    # Print a message indicating the sensor is not touched
    print("Not touched!")

# Initialize a Button object for the touch sensor
# GPIO 17: pin connected to the sensor
# pull_up=None: disable internal pull-up/pull-down resistors
# active_state=True: high voltage is considered the active state
numOfPins = 10
touchPins = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
for pin in numOfPins:
    Button.setmode(Button.BCM)
    Button.setup(touchPins[pin],pull_up=None,active_state=True )
    if touchPins[pin].when_pressed == touched:
        print(pin)
        # lcd.text(pin)

# Assign functions to sensor events

pause()  # Keep the program running to detect touch events