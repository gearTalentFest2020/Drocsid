import tkinter as tkt
import sys, os, socket

contacts = {}

# Function to add a contact
def addContact( name, IP, address):
    pass
# Function to remove a contact
def remContact( IP ):
    pass
# Function to alter a contact
def altContact( name, newName, IP ):
    pass
# Function to save all contacts
def altContact( ):
    pass

print("-------------------------Starting App-------------------------")

open('Contacts.txt', 'w') if(not os.path.exists('Contacts.txt')) else None
contacts_file = open('Contacts.txt', 'r')

# Loading contacts
for line in contacts_file.readlines():
    tokens = line.split()
    assert len(tokens)==2, "Corrupted Contacts File"
    contacts.setdefault(tokens[0], tokens[1])
contacts_file.close()

# Saving contacts
contacts_file = open('Contacts.txt', 'w')
for IP in contacts:
    contacts_file.write(IP + " " + contacts[IP] + '\n')

print("-------------------------Closing App-------------------------")
contacts_file.close()
