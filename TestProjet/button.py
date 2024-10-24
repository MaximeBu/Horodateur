from gpiozero import Button
from time import sleep

# Initialize button connected to GPIO pin 17
buttonBack = Button(20)
buttonNext = Button(21)

# Continuously check the button state
def checkbButtons():
    while True:
        if buttonBack.is_pressed:
            print("Button Back is pressed")  # Print when button is pressed
            ## removeNumber()
            sleep(0.5) 
        elif buttonNext.is_pressed:
            print("Button Next is pressed")  # Print when button is pressed
            ## LCD affiche bonne journée
            sleep(0.5) 
        else:
            print("Button is not pressed")  # Print when button is not pressed
        sleep(0.1) 