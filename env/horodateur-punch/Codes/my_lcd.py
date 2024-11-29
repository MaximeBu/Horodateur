from RPLCD.i2c import CharLCD
from time import sleep
from datetime import datetime
from pytz import timezone

# Initialisation du LCD i2c
lcd = CharLCD(i2c_expander="PCF8574", address= 0x27, port=1, cols=20, rows=2, dotsize=8)
# Nettoyage de l'écran
lcd.clear()

# Fonction pour récupérer l'heure actuelle
def getTime():
  now = datetime.now(timezone("Canada/Eastern"))
  current_time = now.strftime("%Hh:%M")
  return current_time

# Fonction pour récupérer la date actuelle
def getDate():
  now = datetime.now()
  current_date = now.strftime("%d/%m/%y")
  return current_date

# Fonction d'affichage du input pour le code
def show_code_screen(code):
  lcd.clear()
  lcd.write_string("Code: ")
  lcd.write_string(code)

# Fonction d'affichage du menu 1
def show_menu_start():
  lcd.clear()
  lcd.write_string(getTime())
  lcd.write_string("  ")
  lcd.write_string(getDate())
  lcd.crlf()
  lcd.write_string("Choisir de 1 a 4")

# Fonction d'affichage du menu 2
def show_menu_two():
  lcd.clear()
  lcd.write_string("1) Debut travail")
  lcd.crlf()
  lcd.write_string("2) Fin travail")

# Fonction d'affichage du menu 3
def show_menu_three():
  lcd.clear()
  lcd.write_string("3) Debut pause")
  lcd.crlf()
  lcd.write_string("4) Fin pause")

# Fonction d'affichage du menu
def show_menu(menuPosition):
  match menuPosition:
          case 1:
            show_menu_start()
            print("Affichage du menu 1")
          case 2:
            show_menu_two()
            print("Affichage du menu 2")
          case 3:
            show_menu_three()
            print("Affichage du menu 3")
          case _:
            print("Position du menu inexistante")

# Fonction d'affichage d'un message de confirmation
def show_message(option, nom):
  lcd.clear()
  lcd.write_string(nom)
  lcd.write_string(getTime())
  lcd.crlf()

  match option:
    case 1:
      lcd.write_string("Bonne journee!")
      print(nom, " commence sa journée")
    case 2:
      lcd.write_string("Au revoir!")
      print(nom, " a finit sa journée")
    case 3:
      lcd.write_string("Bon repos!")
      print(nom, " prend sa pause")
    case 4:
      lcd.write_string("On y retourne!")
      print(nom, " a finit sa pause")
    case _:
      print("Option inexistante")
  sleep(2)

# Fonction d'affichage de l'erreur
def show_error():
  lcd.clear()
  lcd.write_string("Erreur!")
    
