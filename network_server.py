#!/usr/bin/python3
#coding: utf-8
# Un peu de réseau...
# Executer ce script depuis la commande pour mettre un serveur en attente d'une connexion
import socket
import select

portSocket = 12800
serverName = ""
timeOut = 0.1
NMachineMax = 50

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSocket.bind((serverName,portSocket)) # Serveur prêt à écouter sur le port spécifié
mainSocket.listen(NMachineMax) # Machines max
print("Serveur initialisé")

clientList = []
addrList = []
serverOK = True
while serverOK:
    (newConnexions,trash,trash) = select.select([mainSocket],[],[],timeOut) # On vérifie qu'on n'a pas une nouvelle connexion
    for connexion in newConnexions:
        socket, addr = connexion.accept() # Attente d'une connexion
        print("Une connexion a été établie : {}".format(addr))
        socket.send(b"Connexion OK")
        clientList.append(socket)
        addrList.append(addr)

    waitingClients = [] # Réinitialisation de la liste des clients en attente
    (waitingClients,trash,trash) = select.select(clientList,[],[],timeOut) # On vérifie les ports clients qu'on a ouvert
    for client in waitingClients: # Si certains sont ready to read
        msg = client.recv(1024)
        index = clientList.index(client)
        print("Message reçu de la part de {0} : {1}".format(addrList[index],msg.decode()))
        if msg == b"FIN":
            client.send(b"FIN") # On renvoie un message de fermeture
            client.close() # On ferme la connexion
            del clientList[index] # On supprime ce client de la liste des ports clients ouverts
            del addrList[index] # On supprime ce client de la liste des ports clients ouverts
        elif msg == b"_CLOSE_":
            serverOK = False # On sort de la boucle principale pour arrêter toutes connexions
        else:
            client.send(b"ACK")

print("Fermeture des connexions...")
for client in clientList:
    client.send(b"FIN")
    client.close()
mainSocket.close()
