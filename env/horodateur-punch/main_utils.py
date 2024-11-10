# Option choisit
menuOption = 0
# Nouvelle position recu par le joystick
menuPosition = 1
# Valeur du code entré
code = ""

def getMenuPosition():
  return menuPosition

def getMenuOption():
  return menuOption

def setMenuOption(value):
  global menuOption
  menuOption = value

def setMenuPosition(value):
  global menuPosition
  menuPosition = value

def getCode():
  return code

def setCode(value):
  global code
  code = value
  