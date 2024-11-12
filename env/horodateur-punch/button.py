from gpiozero import Button
from time import sleep

# Initialisation des boutons
# Bouton pour annuler ou supprimer caractère
buttonBack = Button(17)
# Bouton pour confirmer le code
buttonNext = Button(27)

# État du bouton back
buttonBackState = ""
# État du bouton next
buttonNextState = ""


# Fonction de récupération de l'état des boutons
def get_buttons_state():
  return buttonNextState, buttonBackState

def set_button_next_state():
  global buttonNextState
  buttonNextState = "Appuye"

def set_button_back_state():
  global buttonBackState
  buttonBackState = "Appuye"

def set_buttons()
  global buttonBackState, buttonNextState 
  buttonBackState = ""
  buttonNextState = ""

# Fonction qui vérifie si le bouton de retour a été appuyé
def button_back_pressed():
  global buttonBackState
  # Si le bouton est appuyé, on change l'état du bouton
  if buttonBack.is_pressed:
    buttonBackState = "Appuye"
    print("Bouton de retour appuye")


# Fonction qui vérifie si le bouton de confirmation a été appuyé
def button_next_pressed():
  global buttonNextState
  # Si le bouton est appuyé, on change l'état du bouton
  if buttonNext.is_pressed:
    buttonNextState = "Appuye"
    print("Bouton de confirmation appuye")
