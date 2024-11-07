# Documentation: https://alivecode.ca/docs/aliot
import time
import env.led 
import env.joystick

from aliot.aliot_obj import AliotObj

# Attente pour bien établir la communication avec le capteur
time.sleep(5)

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")


def start():
    while True:
        try:
            # Obtenir les données du capteur
            led_state = env.led.get_led_state()
            joystick_value = env.joystick.get_y_axis_value()

            
            # Affichage
            print(f"Led: {led_state}")
            print(f"Joystick: {joystick_value}")

    
            # Envoi des données au serveur ALIVEcode
            horodateur_punch.update_doc({
                "/doc/led": led_state,
                "/doc/joystick_value": joystick_value
            })
            
            # Attente de 1 seconde
            time.sleep(1)
        except KeyboardInterrupt:
            break


# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_start(callback=start)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()