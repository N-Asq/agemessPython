#!/usr/bin/python3
#coding: utf-8
# Un peu de réseau...
# Executer ce script après avoir executé la partie serveur depuis une autre console
import socket

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSocket.connect(("",12800)) # Connexion via le port 12800 du serveur
helloMsg = mainSocket.recv(1024) # On lit le message envoyé par le serveur
print("Message du serveur : {}".format(helloMsg.decode()))

msg = b""
while msg != b"FIN":
    request = input("Veuillez taper un message : ")
    mainSocket.send(request.encode())
    msg = mainSocket.recv(1024)
    print(msg.decode())

print("Fermeture de la connexion...")
mainSocket.close()
