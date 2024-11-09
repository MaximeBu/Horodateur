# Documentation: https://alivecode.ca/docs/aliot
import time
import lcd
import joystick
import touch
import main_utils
import button
import buzzer
import led

from aliot.aliot_obj import AliotObj

# Initialisation des variables
joystick_value = joystick.get_y_axis_value()
menu_position = main_utils.getMenuPosition()
menu_option = main_utils.getMenuOption()
touch = touch.get_touch_number()
buttonNext, buttonBack = button.get_buttons_state()
buzzer_state = buzzer.get_buzzer_state()
led_state = led.get_led_state()
code = main_utils.getCode()

# Attente pour bien établir la communication avec le capteur
time.sleep(5)

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")

def menuPosition1(data): 
    # Get le dictionnaire de logs
    logs = horodateur_punch.get_doc("/doc/logs")
        
    # Ajoute le log dans le dictionnaire
    logs.append({
        "ligne1": lcd.getTime + lcd.getDate,
         "ligne2": "Choisir de 1 à 4"
    })

    horodateur_punch.update_doc({
        "/doc/logs": logs
    })
    time.sleep(1)

def menuPosition2(data): 
    # Get le dictionnaire de logs
    logs = horodateur_punch.get_doc("/doc/logs")
        
    # Ajoute le log dans le dictionnaire
    logs.append({
        "ligne3": "1) Début de travail",
         "ligne4": "2) Fin travail"
    })

    horodateur_punch.update_doc({
        "/doc/logs": logs
    })
    time.sleep(1)

def menuPosition3(data): 
    # Get le dictionnaire de logs
    logs = horodateur_punch.get_doc("/doc/logs")
        
    # Ajoute le log dans le dictionnaire
    logs.append({
        "ligne1": "3) Début Pause",
         "ligne2": "4) Fin Pause"
    })

    horodateur_punch.update_doc({
        "/doc/logs": logs
    })
    time.sleep(1)

def menuCode(data):
    # Get le dictionnaire de logs
    logs = horodateur_punch.get_doc("/doc/logs")
        
    # Ajoute le log dans le dictionnaire
    logs.append({
        "code": "Code : ",
        "numeros": "METTRE LE CODE DU USER AVEC LES BOUTONS"
    })

    horodateur_punch.update_doc({
        "/doc/logs": logs
    })
    time.sleep(1)

# Fonction activer lorsque un bouton touch est appuyé dans l'iterface Aliot
def buttonTouched(data):
    if menu_option == "":
        if data.numero == 1 or data.numero == 2 or data.numero == 3 or data.numero == 4:
            main_utils.setMenuOption(data.numero)
    else:
        if len(code) < 4:
            main_utils.setCode(code + str(data.numero))

# Fonction qui change la valeur du joystick
def joystickChange(data):
    joystick.set_y_axis_value(data.valeur)


def start():
    while True:
        try:
            global joystick_value, menu_position, menu_option, touch, buttonNext, buttonBack, buzzer_state, led_state, code
            # Obtenir les données du capteur
            joystick_value = joystick.get_y_axis_value()
            menu_position = main_utils.getMenuPosition()
            menu_option = main_utils.getMenuOption()
            touch = touch.get_touch_number()
            buttonNext, buttonBack = button.get_buttons_state()
            buzzer_state = buzzer.get_buzzer_state()
            led_state = led.get_led_state()
            code = main_utils.getCode()
            
            # Affichage
            print(f"Joystick: {joystick_value}")
            print(f"Menu Position: {menu_position}")
            print(f"Menu Option: {menu_option}")
            print(f"État du buzzer: {buzzer_state}")
            print(f"État de la LED: {led_state}")
            print(f"Code: {code}")

            if touch != "":
                print(f"Touche appuyé: {touch}")

    
            # Envoi des données au serveur ALIVEcode
            horodateur_punch.update_doc({
                "/doc/joystick_value": joystick_value,
                "/doc/menu_position": menu_position, 
                "/doc/menu_option": menu_option,
                "/doc/touch": touch,
                "/doc/bouton_next": buttonNext,
                "/doc/bouton_back": buttonBack,
                "/doc/buzzer": buzzer_state,
                "/doc/led_state": led_state,
                "/doc/code": code
            })
        
            # Attente de 1 seconde
            time.sleep(1)
        except KeyboardInterrupt:
            break

def menu_change(fields):
    menuPosition = fields['/doc/menuPosition']
    menuOption = fields['/doc/menuOption']
    if menuOption == None: 
        if menuPosition == 1:
            menuPosition1(fields)
        elif menuPosition == 2:
            menuPosition2(fields)
        elif menuPosition3 == 3:
            menuPosition3(fields)   
    else: 
        menuCode(fields)

horodateur_punch.on_start(callback=start)
# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_action_recv("AffichageLCD", callback=menuPosition1)
horodateur_punch.on_action_recv("AffichageLCD", callback=menuPosition2)
horodateur_punch.on_action_recv("AffichageLCD", callback=menuPosition3)
horodateur_punch.on_action_recv("AffichageLCD", callback=menuCode)
horodateur_punch.listen_doc(["/doc/menuPosition"], callback=menu_change)

horodateur_punch.on_action_recv("touched", callback=buttonTouched)
horodateur_punch.on_action_recv("joystick", callback=joystickChange)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
