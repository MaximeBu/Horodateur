# Utilisateurs du système
users = {
  "Maxime" : "1111",
  "Martin" : "2038",
  "Thao" : "9210",
  "Aysha" : "4290",
}

# Fonction de validation du code saisi
def validate_user(code):
  user = ""
  for nom, id in users.items():
    if id == code:
      user = nom
      break
  return user

