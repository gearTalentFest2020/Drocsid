import tkinter as tkt
import sys, os, socket

print("-------------------------Starting App-------------------------")

open('Contacts.txt', 'w') if(not os.path.exists('Contacts.txt')) else None
contacts_file = open('Contacts.txt', 'r+')

print("-------------------------Closing App-------------------------")
contacts_file.close()
#Aditya Chowdhary was not here
#Vyoman was here.
