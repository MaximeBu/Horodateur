# Documentation: https://alivecode.ca/docs/aliot
from aliot.aliot_obj import AliotObj

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")


def start():
    # Écrivez le code que vous voulez exécuter une fois que l'objet
    # est connecté au serveur
    pass


# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_start(callback=start)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
