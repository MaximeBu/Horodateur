# Importations
import serial
from time import sleep
import cam
import joystick
import lcd
import buzzer
import led
import touch
import button
import user


# Pin analogique du joystick
inputPin = "A0"
# Option choisit
menuOption = None
# Dernière position dans le menu
lastMenuPosition = 1
# Nouvelle position recu par le joystick
menuPosition = lastMenuPosition
# Valeur du code entré
code = ""

#Affichage de l'heure
heure = lcd.getTime()
lastTime = heure

# cam.run_camera()

# Affichage de  la page menu initiale
lcd.show_menu_start()
led.turn_off()

# loop until manually stopped
while True:
  try:
    temps = lcd.getTime()
    if temps != heure:
      lastTime = heure
      heure = temps
    # Activation des capteurs touch
    touch.run()
    # Récupération du statut de la led
    ledState = led.get_led_state()
    # Récupération du numéro du capteur touch appuyé
    touchValue = touch.get_touch_number()
    # Réinitialisation de la valeur activeTouch dans le fichier touch
    touch.set_touch_number()
    # Récupération de l'état du buzzer
    buzzer_state = buzzer.get_buzzer_state()
    # Activation des boutons
    button.button_back_pressed()
    button.button_next_pressed()
    # Récupération de l'état des boutons
    boutonNext, boutonBack = button.get_buttons_state()

    if menuOption == None:
      # Changement d'heure dynamiquement sur la page pricipale
      if heure != lastTime and menuPosition == 1:
        lcd.show_menu_start()
        lastTime = heure

      # Récupération de la valeur de l'axe y du joystick
      J = joystick.get_y_axis_value()

      # Choix du menu
      if touchValue == 1 or touchValue == 2 or touchValue == 3 or touchValue == 4:
        menuOption = touchValue

      # Déroulement vers le bas du menu
      if J == 180 and menuPosition < 3:
        menuPosition += 1
      # Déroulement vers le haut du menu
      elif J == 0 and menuPosition > 1:
        menuPosition -= 1

      # Actualisation de la page du menu
      if menuPosition != lastMenuPosition:
        lastMenuPosition = menuPosition
        # Changement de l'affichage
        lcd.show_menu(menuPosition)

    else:
      # Affichage de l'écran demandant la saisie du code de l'employé
      lcd.show_code_screen(code)

      # Si une touche est appuyé, le numéro est affiché
      if touchValue != None and len(code) < 4:
        code += str(touchValue)

      # Si le bouton back est appuyé et que le code est vide, l'écran affiche le menu
      if boutonBack == "Appuyé" and code == "":
        menuOption = None
        lcd.show_menu_start()
      # Si le bouton back est appuyé et que le code possède des chiffres, le dernier chiffre est supprimé
      elif boutonBack == "Appuyé" and len(code) < 5 and len(code) > 0:
        code = code[:len(code)-1]

      # Si le bouton next est appuyé et que le code n'est pas complet, la lumière rouge s'allume et le code se réinitialise
      if boutonNext == "Appuyé" and len(code) < 4:
        led.red()
        code = ""

      # Si le bouton next est appuyé et que le code est remplit, le code est vérifé
      if boutonNext == "Appuyé" and len(code) == 4:
        nom = user.validate_user(code)
	# Si l'utilisateur n'existe pas, il y a erreur
        if nom == "":
            led.red()
        # Si l'utilisateur existe, un message lui est affiché
        else:
          led.green()
          lcd.show_message(menuOption, nom)
          menuOption = None
          lcd.show_menu_start()
        code = ""

    print(inputPin, ":", J, ", Position du menu:", menuPosition, ", Option du menu:", menuOption, ", Led:", ledState, ", Code:", code, ", Buzzer:", buzzer_state, ", Bouton de retour:", boutonBack, ", Bouton de confirmation:", boutonNext, ", heure:", heure)
    sleep(0.2)
  except KeyboardInterrupt:
    break  # stop the while loop

