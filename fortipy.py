import paramiko
import threading
import time
import requests


class fortipy:

    def __init__(self, host="192.168.1.99", username="admin", password="", port=22):

        self.host = host
        self.username = username
        self.password = password

        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Trying to connect to [{}]".format(host))

        try:
            self.client.connect(self.host, username=self.username, password=self.password, port=port)
            print("Connected to [{}]".format(host))
        except:
            print("inpossible to connect to [{}] please verify that SSH is activated or the credentials are corrects")

        
        self.out = self.channel.recv(9999)

    def fistInit(self, newAdminPass):
        '''  Founction to change de default password on first power on '''

        channel = self.client.invoke_shell()
        channel.send('{}\n{}\n'.format(newAdminPass, newAdminPass))
        stdout = self.channel.recv(9999)
        channel.close()

        return stdout

    def createApiToken(self, apiUsername="RTS_Api", apiProfiles="Super_Admin_API"):
        """ Create an API Administrator, an admin profile and generate a Read-Write API token """

        # Creation of the API account
        commands = ["config system accprofile","edit {}".format(apiProfiles),"set secfabgrp read-write","set ftviewgrp read-write","set authgrp read-write","set sysgrp read-write","set netgrp read-write","set loggrp read-write",
    "set fwgrp read-write","set vpngrp read-write","set utmgrp read-write","set wanoptgrp read-write","set wifi read-write","next","end","config system api-user","edit '{}'".format(apiUsername),"set accprofile 'Super_Admin_API'","set vdom 'root'","next","end"]

        for command in commands:
            command = command + "\n"
            self.channel.send(command)


        # Generation du token et récupération de celui ci
        stdin, result, stderr = self.client.exec_command('execute api-user generate-key {}'.format(apiUsername))
        result = str(result.read())
        search = 'New API key: '
        beginIndex = result.find(search)
        token = result[beginIndex + len(search):]
        endIndex = token.find('\\n')
        token = token[:endIndex]
        self.token = token

        return token
    
    def upgrade(self, imageBaseUrl):
        """ 
            Founction that upgrade Fortigate, taking the image from a webserver 
            imageBaseUrl : IP or domain name of the webserver (eg: 192.168.100.12, myserver.mydomain.com)

            The images stored on the server need to be the 6 first letters of the SN (eg: FGT60F.out)

        """
        channel = self.client.invoke_shell()

        # Getting the 6 first letter of the serial number to know what firmware take
        stdin, result, stderr = self.client.exec_command('get system status | grep Serial-Number')
        result = str(result.read())
        index = result.find('FGT')
        if index == -1: # If FGT is not found, trying to search for FWF (Fortiwifi)
            index = result.find('FWF')
        sn = result[index:index+6]
        fileName = sn + '.out'
        url = "http://" + imageBaseUrl + "/" + fileName

        # Working but to debug
        try:
             channel.send('execute restore image url {}\n'.format(url))
             time.sleep(10)
             channel.send('yes')
             time.sleep(25)
             channel.send('y')
             time.sleep(2)
             channel.send('y')
             time.sleep(10)
             print("Upgrade asked, wait for reboot")
             channel.close()

        except:
             print("Can't upgrade the fortigate")