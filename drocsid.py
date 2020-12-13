import tkinter as tk
import sys, os, socket

contacts = {}
backgroundDefault = "#22303c"
btnDefault = "#ffffff"
btnTxtDefault = "#000000"

def getButton( text, command = None, h = 1, w = 48, fontSize = 20):
    temp = tk.Button( master = mainWindow, text = text, font = ("Calibri", fontSize), command = command, bg = btnDefault, fg = btnTxtDefault )
    temp.config( height = h, width = w )
    return temp

# Function to load all contacts
def loadContacts( ):
    pass

# Function to save all contacts
def saveContacts( ):
    pass

# Function to add a contact
def addContact( ):
    promptWindow = tk.Tk()
    promptWindow.title( "Add Contact" )
    promptWindow.geometry( "400x225" )

    name, ID, IP = None, None, None

    nameBox = tk.Entry( master = promptWindow)
    nameBox.insert(string = "Enter Contact name Here", index = 0)

    IPBox = tk.Entry( master = promptWindow)
    IPBox.insert(string = "Enter IP address Here", index = 0)

    IDBox = tk.Entry( master = promptWindow)
    IDBox.insert(string = "Enter Contact name Here", index = 0)

    def temp():
        name, ID, IP = nameBox.get(), IDBox.get(), IPBox.get()

    confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = temp )
    #confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : 1 )

    nameBox.pack()
    IPBox.pack()
    IDBox.pack()

    confirmBtn.pack()

    promptWindow.mainloop()

# Function to remove a contact
def remContact( ):
    promptWindow = tk.Tk()
    promptWindow.title( "Remove Contact" )
    promptWindow.geometry( "400x225" )

# Function to alter a contact
def altContact( ):
    promptWindow = tk.Tk()
    promptWindow.title( "Edit Contact" )
    promptWindow.geometry( "400x225" )

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
addContactBtn = getButton("Add Contact", command = addContact)
remContactBtn = getButton("Remove Contact", command = remContact)
altContactBtn = getButton("Edit Contact", command = altContact )
selRoomBtn = getButton("Select Chatroom")

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
