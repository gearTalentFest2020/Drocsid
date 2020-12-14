import tkinter as tk
import sys, os, socket

contacts = {}
backgroundDefault = "#22303c"
btnDefault = "#ffffff"
btnTxtDefault = "#000000"

# Helper functions
def _dicset( dic, key, val):
    dic[key] = val

# Wrapper around windows
def getWindow( title, geometry ):
    temp = tk.Tk()
    temp.title( title )
    temp.geometry( geometry )
    return temp

# Wrapper around buttons
def getButton( text, command = None, h = 1, w = 48, fontSize = 20):
    temp = tk.Button( master = mainWindow, text = text, font = ("Calibri", fontSize), command = command, bg = btnDefault, fg = btnTxtDefault )
    temp.config( height = h, width = w )
    return temp

# Function to load all contacts
def loadContacts( ):
    open('Contacts.txt', 'w') if(not os.path.exists('Contacts.txt')) else None
    contacts_file = open('Contacts.txt', 'r')

    for line in contacts_file.readlines():
        tokens = line.split(';')
        tokens[2] = tokens[2][:-1]
        assert len(tokens)==3, "Corrupted Contacts File"
        contacts.setdefault(tokens[0], [tokens[1], tokens[2]])
    contacts_file.close()

# Function to save all contacts
def saveContacts( ):
    contacts_file = open('Contacts.txt', 'w')
    for ID in contacts: contacts_file.write(ID + ";" + contacts[ID][0] + ";" + contacts[ID][1] + '\n')

# Function to add a contact
def addContact( ):

    promptWindow = getWindow( "Add Contact", "400x225" )

    name = tk.Entry( master = promptWindow)
    name.insert(string = "Name", index = 0)

    ip = tk.Entry( master = promptWindow)
    ip.insert(string = "IP", index = 0)

    ID = tk.Entry( master = promptWindow)
    ID.insert(string = "ID", index = 0)


    confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.setdefault( ID.get().strip(), [name.get().strip(), ip.get().strip()] ) and promptWindow.destroy() )

    name.pack()
    ip.pack()
    ID.pack()

    confirmBtn.pack()

    promptWindow.mainloop()

# Function to remove a contact
def remContact( ):

    promptWindow = getWindow( "Remove Contact", "400x225" )

    ID = tk.Entry( master = promptWindow)
    ID.insert(string = "ID", index = 0)

    confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.pop(ID.get().strip()) and promptWindow.destroy() )

    ID.pack()
    confirmBtn.pack()

    promptWindow.mainloop()

# Function to alter a contact
def altContact( ):

    promptWindow = getWindow( "Edit Contact", "400x225" )

    ID = tk.Entry( master = promptWindow)
    ID.insert(string = "ID", index = 0)

    name = tk.Entry( master = promptWindow)

    ip = tk.Entry( master = promptWindow)

    confirmBtn1 = tk.Button( master = promptWindow, text = "Edit", font = ("Calibri", 12), command = lambda : name.insert(string = contacts[ID.get().strip()][0], index = 0) or ip.insert(string = contacts[ID.get().strip()][1], index = 0) )
    confirmBtn2 = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : _dicset( contacts, ID.get().strip(), [name.get(), ip.get()] ) or promptWindow.destroy() )

    ID.pack()
    name.pack()
    ip.pack()

    confirmBtn1.pack()
    confirmBtn2.pack()

    promptWindow.mainloop()

def createChatroom( name ):

    name = "chatroom__" + name

    try: os.mkdir( name )
    except: pass

    open(name + '/People.txt', 'w') if(not os.path.exists(name + '/People.txt')) else None
    open(name + '/Chats.txt', 'w') if(not os.path.exists(name + '/Chats.txt')) else None


print("-------------------------Starting App-------------------------")

open('Contacts.txt', 'w') if(not os.path.exists('Contacts.txt')) else None
contacts_file = open('Contacts.txt', 'r')

# Loading contacts
loadContacts()

# Creating window
mainWindow = getWindow( "Drocsid", "800x450" )

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

createChatroom("Test1")

saveContacts()

print("-------------------------Closing App-------------------------")
contacts_file.close()