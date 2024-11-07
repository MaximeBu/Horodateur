# Documentation: https://alivecode.ca/docs/aliot
from aliot.aliot_obj import AliotObj
import time

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")

# Fonction qui sera appelée pour allumer la led
def touched(data):
    print("Bouton cliqué")
    #buzzer_component.on()
    horodateur_punch.update_component("Mybuzzer", 500)
    time.sleep(1)
    
# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_action_recv(action_id="touch", callback=touched)


# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
