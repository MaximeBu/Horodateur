import serial
import time
import threading

# Création de la connexion serial
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.flushInput()

# Attendre que la communication serial s'établie
time.sleep(2)

# Valeur de l'axe y du joystick
yAxisValue = 90
distance = 0
powerMode = True

# Récupération de la valeur de l'axis y du joystick
def get_joystick():
  return yAxisValue

def get_distance():
  return distance

def get_powerMode():
  return powerMode

# Récupération des données dans la ligne du serial
def read_data():
  joystick, distance, powerMode = ser.readline().decode().strip().split(":")
  return float(joystick), float(distance), int(powerMode)


# Lecture des donées dans le serial
def read_from_serial():
  global yAxisValue, powerMode, distance

  try:
    ser.flush()
    while True:
      if ser.in_waiting > 0:
        # Attribution de la valeur
        yAxisValue, distance, powerMode = read_data()
  except KeyboardInterrupt:
    print("Exiting...")
  finally:
    ser.close()


try:
  t= threading.Thread(target=read_from_serial)
  t.start()
except KeyboardInterrupt:
  print("Exiting...")