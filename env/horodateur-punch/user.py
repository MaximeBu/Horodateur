# Utilisateurs du système
users = {
  "Maxime Bureau" : "1111",
  "Martin Ndjiya" : "2038",
  "Thao Chi Tran" : "9210",
  "Aysha Hossain" : "4290",
}

nom = ""

# Fonction qui récupère le nom de l'utilisateur qui se connecte
def getNom():
  return nom

# Fonction qui attribut le nom de l'utilisateur qui se connecte
def setNom(newName):
  global nom
  nom = newName

# Fonction de validation du code saisi
def validate_user(code):
  for nom, id in users.items():
    if id == code:
      setNom(nom)
      break

