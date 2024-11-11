# Documentation: https://alivecode.ca/docs/aliot
import time
import led
import lcd
import joystick
import touch
import main_utils
import button
import buzzer
import led
import user

from aliot.aliot_obj import AliotObj

# Initialisation des variables
joystick_value = joystick.get_y_axis_value()
menu_position = main_utils.getMenuPosition()
menu_option = main_utils.getMenuOption()
touch_num = touch.get_touch_number()
buttonNext, buttonBack = button.get_buttons_state()
buzzer_state = buzzer.get_buzzer_state()
led_state = led.get_led_state()
code = main_utils.getCode()
led_color = led.get_led_color()
user_n = user.getNom()

# Attente pour bien établir la communication avec le capteur
time.sleep(5)

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")

def menuPosition(data): 
    if menu_position == 1:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "Choisir de 1 à 4")

    elif menu_position == 2:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "1) Début de travail")
        horodateur_punch.update_component("AffichageLCD", "2) Fin travail")

    elif menu_position == 3:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", "3) Début Pause")
        horodateur_punch.update_component("AffichageLCD", "4) Fin Pause")
    time.sleep(1)

def menuCode(data):
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Code: "+ code)
    time.sleep(1)

# Fonction activée lorsque un bouton touch est appuyé dans l'iterface Aliot
def buttonTouched(data):
    if menu_option == 0:
        if data["numero"] == 1 or data["numero"] == 2 or data["numero"] == 3 or data["numero"] == 4:
            main_utils.setMenuOption(data["numero"])
    else:
        if data["numero"] != "" and len(code) < 4:
            newCode = code + str(data["numero"])
            main_utils.setCode(newCode)

    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Touche appuyé: " + str(data["numero"]))
    horodateur_punch.update_component("Mybuzzer", 500)
    time.sleep(1)

# Fonction qui change la valeur du joystick
def joystickChange(data):
    joystick.set_y_axis_value(data.value)

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
    time.sleep(1)

# Fonction activée lorsque la lumière est allumée et rouge
def sendError(data):
    # Ajoute le log dans le dictionnaire
    horodateur_punch.update_component("AffichageLCD", "Erreur")
    time.sleep(1)

# Fonction activée lorsque la lumière est allumée et verte
def sendSuccess(data):
    horodateur_punch.update_component("AffichageLCD", nom)
    if menu_option == 1:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + "commence sa journée")
    elif menu_option == 2:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " a finit sa journée")
    elif menu_option == 3:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " prend sa pause")
    elif menu_option == 4:
        # Ajoute le log dans le dictionnaire
        horodateur_punch.update_component("AffichageLCD", nom + " a finit sa pause")
    time.sleep(1)

    
# Programme principal
def start():
    while True:
        try:
            global joystick_value, menu_position, menu_option, touch_num, buttonNext, buttonBack, buzzer_state, led_state, code, led_color
            # Obtenir les données du capteur
            joystick_value = joystick.get_y_axis_value()
            menu_position = main_utils.getMenuPosition()
            menu_option = main_utils.getMenuOption()
            touch_num = touch.get_touch_number()
            buttonNext, buttonBack = button.get_buttons_state()
            buzzer_state = buzzer.get_buzzer_state()
            led_state = led.get_led_state()
            led_color = led.get_led_color()
            code = main_utils.getCode()
            user_n = user.getNom()
            
            # Affichage
            print(f"Joystick: {joystick_value}")
            print(f"Menu Position: {menu_position}")
            print(f"Menu Option: {menu_option}")
            print(f"État du buzzer: {buzzer_state}")
            print(f"État de la LED: {led_state}")
            print(f"Couleur de la LED: {led_color}")

            if touch_num != "":
                print(f"Touche appuyé: {touch_num}")

            if user_n != "":
                print(f"Nom de l'utilisateur: {user_n}")

            if code != "":
                print(f"Code: {code}")

    
            # Envoi des données au serveur ALIVEcode
            horodateur_punch.update_doc({
                "/doc/joystick_value": joystick_value,
                "/doc/menu_position": menu_position, 
                "/doc/menu_option": menu_option,
                "/doc/touch": touch_num,
                "/doc/bouton_next": buttonNext,
                "/doc/bouton_back": buttonBack,
                "/doc/buzzer": buzzer_state,
                "/doc/led/led_state": led_state,
                "/doc/led/couleur": led_color,
                "/doc/code": code
            })

            # Déroulement vers le bas du menu
            if joystick_value <= 180 and joystick_value >= 170 and menu_position < 3:
                newMenuPosition = menu_position + 1
                main_utils.setMenuPosition(newMenuPosition)
            # Déroulement vers le haut du menu
            elif joystick_value >= 0 and joystick_value <= 10 and menu_position > 1:
                newMenuPosition = menu_position - 1
                main_utils.setMenuPosition(newMenuPosition)

            # Si le bouton back est appuyé et que le code est vide, l'écran affiche le menu
            if buttonBack == "Appuyé" and code == "":
                main_utils.setMenuOption(0)

            # Si le bouton back est appuyé et que le code possède des chiffres, le dernier chiffre est supprimé
            elif buttonBack == "Appuyé" and len(code) < 5 and len(code) > 0:
                newCode = code[:len(code)-1]
                main_utils.setCode(newCode)

            # Si le bouton next est appuyé et que le code n'est pas complet, la lumière rouge s'allume et le code se réinitialise
            if buttonNext == "Appuyé" and len(code) < 4:
                led.red()
                led.get_led_color()

            # Si le bouton next est appuyé et que le code est remplit, le code est vérifé
            if buttonNext == "Appuyé" and len(code) == 4:
                user.validate_user(code)
                led.get_led_color()
                # Si l'utilisateur n'existe pas, il y a erreur
                if user_n == "":
                    led.red()
                    led.get_led_color()
                    led.turn_off()
                # Si l'utilisateur existe, un message lui est affiché
                else:
                    led.green()
                    led.get_led_color()
                    main_utils.setMenuOption(0)
                    user.setNom("")
                    main_utils.setCode("")

            # Attente de 1 seconde
            time.sleep(1)
        except KeyboardInterrupt:
            break

horodateur_punch.on_start(callback=start)
# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_action_recv("AffichageLCD", callback=menuPosition)
horodateur_punch.on_action_recv("erreur", callback=sendError)
horodateur_punch.on_action_recv("succes", callback=sendSuccess)
horodateur_punch.on_action_recv("sendCode", callback=menuCode)
horodateur_punch.on_action_recv("touched", callback=buttonTouched)
horodateur_punch.on_action_recv("joystick", callback=joystickChange)
horodateur_punch.on_action_recv("boutonNext", callback=buttonNextAction)
horodateur_punch.on_action_recv("boutonBack", callback=buttonBackAction)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
