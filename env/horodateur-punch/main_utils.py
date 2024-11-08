# Option choisit
menuOption = None
# Nouvelle position recu par le joystick
menuPosition = 1

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
  