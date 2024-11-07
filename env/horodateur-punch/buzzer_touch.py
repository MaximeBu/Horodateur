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
horodateur_punch.on_action_recv(action_id="touch0", callback=touched)
horodateur_punch.on_action_recv(action_id="touch1", callback=touched)
horodateur_punch.on_action_recv(action_id="touch2", callback=touched)
horodateur_punch.on_action_recv(action_id="touch3", callback=touched)
horodateur_punch.on_action_recv(action_id="touch4", callback=touched)
horodateur_punch.on_action_recv(action_id="touch5", callback=touched)
horodateur_punch.on_action_recv(action_id="touch6", callback=touched)
horodateur_punch.on_action_recv(action_id="touch7", callback=touched)
horodateur_punch.on_action_recv(action_id="touch8", callback=touched)
horodateur_punch.on_action_recv(action_id="touch9", callback=touched)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
