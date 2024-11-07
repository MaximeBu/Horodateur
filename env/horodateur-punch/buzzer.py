import RPi.GPIO as GPIO
from time import sleep

# Pin utilisé sur le raspberry pi
buzzer = 21

# Paramètre du GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

# État du buzzer
buzzerState = "Éteint"


# Récupération de l'état du buzzer
def get_buzzer_state():
  return buzzerState


# Fonction qui active un son lorsqu'une touche est activée
def touch_sound():
  global buzzerState
  buzz = GPIO.PWM(buzzer, 300)
  buzz.start(50)
  buzzerState = "Activé"
  sleep(0.2)
  buzz.stop()
  buzzerState = "Éteint"
