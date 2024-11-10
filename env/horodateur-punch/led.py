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
ledState = False
# Coleur de la Led
ledColor = ""

# Configuration des pins GPIO
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)


# Fonction pour récupérer la valeur de la Led
def get_led_state():
  return ledState

def get_led_color():
  return ledColor

# Fonction pour fermer les lumières
def turn_off():
  global ledState
  global ledColor
  print("Lumière éteinte")
  GPIO.output(redPin, GPIO.LOW)
  GPIO.output(greenPin, GPIO.LOW)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = False
  ledColor = ""


# Fonction pour allumer une lumière rouge
def red():
  global ledState
  global ledColor
  print("ERREUR!!!")
  GPIO.output(redPin, GPIO.HIGH)
  GPIO.output(greenPin, GPIO.LOW)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = True
  ledColor = "rouge"
  sleep(2)
  turn_off()


# Fonction pour allumer une lumière verte
def green():
  global ledState
  global ledColor
  print("SUCCES!!!")
  GPIO.output(redPin, GPIO.LOW)
  GPIO.output(greenPin, GPIO.HIGH)
  GPIO.output(bluePin, GPIO.LOW)
  ledState = True
  ledColor = "vert"
  sleep(2)
  turn_off()