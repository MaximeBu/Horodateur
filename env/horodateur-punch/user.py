# Utilisateurs du système
users = {
  "Maxime" : "1111",
  "Martin" : "2038",
  "Thao" : "9210",
  "Aysha" : "4290",
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

