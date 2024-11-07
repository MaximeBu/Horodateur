# Documentation: https://alivecode.ca/docs/aliot
from aliot.aliot_obj import AliotObj
import env.lcd
import time

# Création de l'objet à partir du fichier de configuration
horodateur_punch = AliotObj("horodateur-punch")


def start():
    while True:
        try:
            # Get le dictionnaire de logs
            logs = horodateur_punch.get_doc("/doc/logs")
            
            # Ajoute le log dans le dictionnaire
            logs.append({
                "date": env.lcd.getTime,
                "time": env.lcd.getDate
            })
            horodateur_punch.update_doc({
                "/doc/logs": logs
            })
            time.sleep(1)


        except KeyboardInterrupt:
            break


# Appel de la fonction start une fois que l'objet se connecte au serveur
horodateur_punch.on_start(callback=start)

# Connection de l'objet au serveur ALIVEcode
horodateur_punch.run()
