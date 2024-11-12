# Importations
import serial
from time import sleep
# import cam
import joystick
import lcd
import buzzer
import led
import touch
import button
import user
import main_utils

from aliot.aliot_obj import AliotObj

# Pin analogique du joystick
inputPin = "A0"
# Dernière position dans le menu
lastMenuPosition = main_utils.getMenuPosition()

#Affichage de l'heure
heure = lcd.getTime()
lastTime = heure

# cam.run_camera()

# Affichage de  la page menu initiale
lcd.show_menu_start()
led.turn_off()

# loop until manually stopped

# Attente pour bien établir la communication avec le capteur
sleep(5)

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")

# Fonction activée lorsque le bouton next est appuyé dans l'iterface Aliot
def buttonNextAction(data):
    button.set_button_next_state()
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Bouton next appuyé")

# Fonction activée lorsque le bouton back est appuyé dans l'iterface Aliot
def buttonBackAction(data):
    button.set_button_back_state()
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Bouton back appuyé")
    sleep(1)

# Fonction activée lorsque la lumière est allumée et rouge
def sendError(data):
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Erreur")
    sleep(1)

# Fonction activée lorsque la lumière est allumée et verte
def sendSuccess(data):
    horodateur_punch.update_component("AffichageLCD", nom)
    if main_utils.getMenuOption() == 1:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + "commence sa journée")
    elif main_utils.getMenuOption() == 2:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " a finit sa journée")
    elif main_utils.getMenuOption() == 3:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " prend sa pause")
    elif main_utils.getMenuOption() == 4:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " a finit sa pause")
    sleep(1)

def menuPosition(data):
    if main_utils.getMenuPosition() == 1:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "Choisir de 1 à 4")

    elif main_utils.getMenuPosition() == 2:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "1) Début de travail")
        horodateur_punch.update_component("AffichageLCD", "2) Fin travail")

    elif main_utils.getMenuPosition() == 3:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "3) Début Pause")
        horodateur_punch.update_component("AffichageLCD", "4) Fin Pause")
    sleep(1)

def menuCode(data):
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Code: "+ code)
    sleep(1)

def start():
  while True:
    try:
      temps = lcd.getTime()
      if temps != heure:
        lastTime = heure
        heure = temps
      # Activation des capteurs touch
      touch.run()
      # Récupération du statut de la led
      led_state = led.get_led_state()
      led_color = led.get_led_color()
      # Récupération du numéro du capteur touch appuyé
      touch_num = touch.get_touch_number()
      # Réinitialisation de la valeur activeTouch dans le fichier touch
      touch.set_touch_number()
      # Récupération de l'état du buzzer
      buzzer_state = buzzer.get_buzzer_state()
      # Activation des boutons
      button.button_back_pressed()
      button.button_next_pressed()
      # Récupération de l'état des boutons
      bouton_next, bouton_back = button.get_buttons_state()
      # Récupération de la valeur de l'option choisit
      menu_option = main_utils.getMenuOption()
      # Récupération de la valeur de la position du menu active
      menu_position = main_utils.getMenuPosition()
      # Récupération du code de l'employé
      code = main_utils.getCode()
      # Récupération du nom de l'employé
      nom = user.getNom()

      if menu_option == 0:
        # Changement d'heure dynamiquement sur la page pricipale
        if heure != lastTime and menu_position == 1:
          lcd.show_menu_start()
          lastTime = heure

        # Récupération de la valeur de l'axe y du joystick
        joystick_value = joystick.get_y_axis_value()

        # Choix du menu
        if touch_num == 1 or touch_num == 2 or touch_num == 3 or touch_num == 4:
          main_utils.setMenuOption(touch_num)

        # Déroulement vers le bas du menu
        if joystick_value <= 180 and joystick_value >= 170 and menu_position < 3:
          newMenuPosition = menu_position + 1
          main_utils.setMenuPosition(newMenuPosition)
        # Déroulement vers le haut du menu
        elif joystick_value >= 0 and joystick_value <= 10 and menu_position > 1:
          newMenuPosition = menu_position - 1
          main_utils.setMenuPosition(newMenuPosition)

        # Actualisation de la page du menu
        if menu_position != lastMenuPosition:
          lastMenuPosition = menu_position
          # Changement de l'affichage
          lcd.show_menu(menu_position)

      else:
        # Affichage de l'écran demandant la saisie du code de l'employé
        lcd.show_code_screen(code)

        # Si une touche est appuyé, le numéro est affiché
        if touch_num != "" and len(code) < 4:
          newCode = code + str(touch_num)
          main_utils.setCode(newCode)

        # Si le bouton back est appuyé et que le code est vide, l'écran affiche le menu
        if bouton_back == "Appuyé" and code == "":
          main_utils.setMenuOption(0)
          lcd.show_menu_start()
        # Si le bouton back est appuyé et que le code possède des chiffres, le dernier chiffre est supprimé
        elif bouton_back == "Appuyé" and len(code) < 5 and len(code) > 0:
          newCode = code[:len(code)-1]
          main_utils.setCode(newCode)

        # Si le bouton next est appuyé et que le code n'est pas complet, la lumière rouge s'allume et le code se réinitialise
        if bouton_next == "Appuyé" and len(code) < 4:
          led.red()
          main_utils.setCode("")

        # Si le bouton next est appuyé et que le code est remplit, le code est vérifé
        if bouton_next == "Appuyé" and len(code) == 4:
          user.validate_user(code)
          nom = user.getNom()
          # Si l'utilisateur n'existe pas, il y a erreur
          if nom == "":
              led.red()
          # Si l'utilisateur existe, un message lui est affiché
          else:
            led.green()
            lcd.show_message(menu_option, nom)
            main_utils.setMenuOption(0)
            lcd.show_menu_start()
            user.setNom("")
          main_utils.setCode("")


      print(f"Joystick: {joystick_value}")
      print(f"Menu Position: {menu_position}")
      print(f"Menu Option: {menu_option}")
      print(f"État du buzzer: {buzzer_state}")
      print(f"État de la LED: {led_state}")
      print(f"Couleur de la LED: {led_color}")
      print(f"État du bouton next: {bouton_next}")
      print(f"État du bouton back: {bouton_back}")
      print(f"Touche appuyé: {touch_num}")
      print(f"Nom de l'utilisateur: {nom}")
      print(f"Code: {code}")

      # print(inputPin, ":", J, ", Position du menu:", menuPosition, ", Option du menu:", menuOption, ", Led:", ledState, ", Code:", code, ", Buzzer:", buzzer_state, ", Bouton de retour:", boutonBack, ", Bouton de confirmation:", boutonNext, ", heure:", heure)
      # Envoi des données au serveur ALIVEcode
      horodateur_punch.update_doc({
        "/doc/joystick_value": joystick_value,
        "/doc/menu_position": menu_position, 
        "/doc/menu_option": menu_option,
        "/doc/touch": touch_num,
        "/doc/bouton_next": bouton_next,
        "/doc/bouton_back": bouton_back,
        "/doc/buzzer": buzzer_state,
        "/doc/led/led_state": led_state,
        "/doc/led/couleur": led_color,
        "/doc/code": code
      })
      sleep(0.2)
    except KeyboardInterrupt:
      break  # stop the while loop



horodateur_punch.on_start(callback=start)
# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_action_recv("AffichageLCD", callback=menuPosition)
horodateur_punch.on_action_recv("erreur", callback=sendError)
horodateur_punch.on_action_recv("succes", callback=sendSuccess)
horodateur_punch.on_action_recv("sendCode", callback=menuCode)
horodateur_punch.on_action_recv("touched", callback=lambda data: touch.set_touch_number(data["numero"]))
horodateur_punch.on_action_recv("joystick", callback=lambda data: joystick.set_y_axis_value(data["valeur"]))
horodateur_punch.on_action_recv("boutonNext", callback=buttonNextAction)
horodateur_punch.on_action_recv("boutonBack", callback=buttonBackAction)


# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
