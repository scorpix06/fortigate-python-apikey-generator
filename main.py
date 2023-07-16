import fortipy

##### Variables ####

ip = "192.168.1.99"
user = "admin"
password = ""
portSSH = 22
newPassword = "NOUVEAUMOTDEPASSE"

httpServer = "192.168.40.112" # Adresse IP du serveur web contenant les fichier d'OS

apiProfileName = "Super_Admin_API"
apiUserName = "RTS_Api"

####################

config = fortipy(ip, user, password, portSSH)
config.fisrtInit(newPassword)
config.upgrade(httpServer)


