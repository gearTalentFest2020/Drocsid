import tkinter as tk
import sys, os, socket

contacts = {}
backgroundDefault = "#22303c"

# Function to load all contacts
def loadContacts( ):
    pass
# Function to add a contact
def addContact( ID, name, IP ):
    pass
# Function to remove a contact
def remContact( ID ):
    pass
# Function to alter a contact
def altContact( ID, new ):
    pass
# Function to save all contacts
def saveContact( ):
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

# Creating window
mainWindow = tk.Tk()
mainWindow.title( "Drocsid" )
mainWindow.geometry( "800x450" )

# mainWindow.configure(bg=_from_rgb((0, 10, 255)))
mainWindow.configure( bg = backgroundDefault )
addContactBtn = tk.Button( master = mainWindow, text = "Add Contact", command = None )
remContactBtn = tk.Button( master = mainWindow, text = "Remove Contact", command = None )
altContactBtn = tk.Button( master = mainWindow, text = "Edit Contact", command = None )
selRoomBtn = tk.Button( master = mainWindow, text = "Select chatroom", command = None )

addContactBtn.pack()
remContactBtn.pack()
altContactBtn.pack()
selRoomBtn.pack()

mainWindow.mainloop()

# Saving contacts
contacts_file = open('Contacts.txt', 'w')
for IP in contacts:
    contacts_file.write(IP + " " + contacts[IP] + '\n')

print("-------------------------Closing App-------------------------")
contacts_file.close()
