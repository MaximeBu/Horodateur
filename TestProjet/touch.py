from gpiozero import Button
from signal import pause

# Function called when the sensor is touched
def touched(num):
    # Print a message indicating the sensor is touched
    print(f"Touched! {num}")

# Function called when the sensor is not touched
def not_touched(num):
    # Print a message indicating the sensor is not touched
    print(f"Not touched! {num}")

# Initialize a Button object for the touch sensor
# GPIO 17: pin connected to the sensor
# pull_up=None: disable internal pull-up/pull-down resistors
# active_state=True: high voltage is considered the active state
touchPins = {
    1: 17, 
    2: 27, 
    3: 22, 
    4: 11, 
    5: 13, 
    6: 15, 
    7: 19, 
    8: 21, 
    9: 23, 
    0: 18
}


def touchSensors():
    for num, pin in touchPins.items():
        button = Button(pin, pull_up=True)
        button.when_pressed = lambda n=num: touched(n)
        button.when_released = lambda n=num: not_touched(n)

# Assign functions to sensor events

pause()  # Keep the program running to detect touch events