import random
import os
import paramiko

"""
Author: Mustafa Choueib
Last Revision Date: March 23rd, 2023.
Purpose: The purpose of this script is to gather the desired configurations from the GUI,
         and pass those inputs off to the Server, ML Blackboard and front end script.
"""

def connectToServer():
    serverIP = "172.105.14.186"
    serverUsername = "root"
    serverPassword = "Mobichargedgroup"
    serverPort = 22

    try:
        ssh = paramiko.SSHClient()
        #Load SSH hot keys
        ssh.load_system_host_keys()
        #Add SSH host key automatically if needed.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Connect to the server
        ssh.connect(serverIP, serverPort, serverUsername, serverPassword, look_for_keys=False)

        #Setting the path to the correct directory
        pathCommand = "cd Mobicharged-Server"
        stdin, stdout, stderr = ssh.exec_command(pathCommand)

        #Sending the batch file to the remote server
        sftp = ssh.open_sftp()
        sftp.put("launch_server.bat", '//root//Mobicharged-Server//launch_server.bat')
        sftp.close()

        permCommand = "chmod +x launch_server.bat"
        stdin, stdout, stderr = ssh.exec_command(permCommand)
        #stdin, stdout, stderr = ssh.exec_command("./launch_server.bat")
    except Exception as e:
        return False

def createLaunchBat(inputSize, outputSize, inputList, simFilePath):
    #Need to indentify the chosen simulation file to the server so it can inform any clients trying to connect.
    fileName = os.path.basename(simFilePath)
    #Dynamically creating a bat file consisting of the inputs specified in the GUI
    launchBat = open('launch_server.bat', 'w+')
    #launchBat.write("#!/bin/sh\n")
    launchBat.write('''@echo off
    python3 -c "from server_initializer import startServer ; startServer({0}, {1}, {2}, '{3}')"
    pause
    '''.format(inputSize, outputSize, inputList, fileName))
    launchBat.close()

    connectToServer()


#Initializes the Server Socket with the given configuration
def startServer(inputSize, outputSize, inputList, simFileName):
    import server
    server.Server_Configuration(inputSize,outputSize, inputList, simFileName)

