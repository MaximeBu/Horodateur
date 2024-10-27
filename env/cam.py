from picamera2 import Picamera2, Preview, MappedArray
import time
from IPython.display import clear_output
from matplotlib import pyplot as plt

# Initialisation de l'objet Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)

# Délaisse la ressource caméra au cas où elle serait utilisée
try :
  picam2.stop()
except:
  print("ok")

picam2.start()
print("Caméra en marche")
# Laisse le temps à la camera de se preparer
time.sleep(0.2)

# Fonction qui récupère l'image de la caméra pour ensuite l'utiliser
def run_camera():
  try:
    img = picam2.capture_array()
    plt.axis("off")
    plt.title("Video test")
    #plt.imshow(img)
    #plt.show()    
    clear_output()
  except:
    picam2.stop()
    print("Released video resource")

