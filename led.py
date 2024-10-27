import RPi.GPIO as GPIO
from time import sleep

# Configuration du GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pins du raspberry pi utilisée pour les branches de la Led
redPin = 26
greenPin = 20
bluePin = 16

# État de la Led
ledState = "Off"

# Configuration des pins GPIO
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)


# Fonction pour récupérer la valeur de la Led
def get_led_state():
  return ledState


# Fonction pour fermer les lumières
def turn_off():
  print("Lumière éteinte")
  GPIO.output(redPin, GPIO.LOW)
  GPIO.output(greenPin, GPIO.LOW)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = "Off"


# Fonction pour allumer une lumière rouge
def red():
  print("ERREUR!!!")
  GPIO.output(redPin, GPIO.HIGH)
  GPIO.output(greenPin, GPIO.LOW)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = "Rouge"
  sleep(2)
  turn_off()


# Fonction pour allumer une lumière verte
def green():
  print("SUCCES!!!")
  GPIO.output(redPin, GPIO.LOW)
  GPIO.output(greenPin, GPIO.HIGH)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = "Vert"
  sleep(2)
  turn_off()
