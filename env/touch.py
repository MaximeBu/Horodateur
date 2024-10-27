from gpiozero import Button
import buzzer

# Capteurs de touchés
touch_numero_1 = Button(18)
touch_numero_2 = Button(23)
touch_numero_3 = Button(22)
touch_numero_4 = Button(24)
touch_numero_5 = Button(25)
touch_numero_6 = Button(12)
touch_numero_7 = Button(5)
touch_numero_8 = Button(6)
touch_numero_9 = Button(13)
touch_numero_0 = Button(19)

# Valeur du bouton touché
activeTouch= None


# Function called when the sensor is touched
def touched(num):
  global activeTouch
  activeTouch = num
  # Affichage du numéro appuyé
  print(f"Touched! {num}")
  # Activation du bruit lorsqu'il est appuyé
  buzzer.touch_sound()


# Fonction pour réinitialiser activeButton
def set_touch_number():
  global activeTouch
  activeTouch = None


# Fonction qui récupère la valeur du activeButton
def get_touch_number():
  return activeTouch


# Fonction qui vérifie si un bouton a été touché
def run():
  touch_numero_1.when_pressed = lambda : touched(1)
  touch_numero_2.when_pressed = lambda : touched(2)
  touch_numero_3.when_pressed = lambda : touched(3)
  touch_numero_4.when_pressed = lambda : touched(4)
  touch_numero_5.when_pressed = lambda : touched(5)
  touch_numero_6.when_pressed = lambda : touched(6)
  touch_numero_7.when_pressed = lambda : touched(7)
  touch_numero_8.when_pressed = lambda : touched(8)
  touch_numero_9.when_pressed = lambda : touched(9)
  touch_numero_0.when_pressed = lambda : touched(0)
