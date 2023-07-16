import fortipy

##### Variables ####

ip = "192.168.1.99"
user = "admin"
password = ""
portSSH = 22
newPassword = "NEWPASSWORD"

httpServer = "192.168.40.112" # IP address or FQDN of the webserver containing the images

apiProfileName = "Super_Admin_API"
apiUserName = "RTS_Api"

####################

config = fortipy(ip, user, password, portSSH)
config.fisrtInit(newPassword)
config.createApiToken(apiUserName, apiProfileName)
config.upgrade(httpServer)


