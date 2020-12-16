import tkinter as tk
import sys, os, socket
import contacts

import selectors

from theme import *

contacts = contacts.contactsManager()

# Create a socket
sock = socket.socket()
socketSelector = selectors.DefaultSelector()

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

# Function to add a contact
def addContact( ):

    addContactFrame = tk.Frame( master = mainWindow )

    name = tk.Entry( master = addContactFrame)
    name.insert(string = "Enter contact's name", index = 0)

    ID = tk.Entry( master = addContactFrame)
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = addContactFrame, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.addContact( ID.get(), name.get()) or addContactFrame.destroy() )

    name.pack()
    ID.pack()

    confirmBtn.pack()
    addContactFrame.grid( row = 0, column = 1 )

# Function to remove a contact
def remContact( ):

    remContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = remContactFrame)
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = remContactFrame, text = "Remove", font = ("Calibri", 12), command = lambda : contacts.remContact(ID.get()) or remContactFrame.destroy() )

    ID.pack()
    confirmBtn.pack()

    remContactFrame.grid( row = 0, column = 1 )

# Function to alter a contact
def altContact( ):

    altContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = altContactFrame )
    ID.insert(string = "Enter contact's ID", index = 0)

    name = tk.Entry( master = altContactFrame )

    confirmBtn1 = tk.Button( master = altContactFrame, text = "Edit", font = ("Calibri", 12), command = lambda : name.insert(string = contacts[ID.get().strip()], index = 0))
    confirmBtn2 = tk.Button( master = altContactFrame, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.altContact( ID.get(), name.get() ) or altContactFrame.destroy())

    ID.pack()
    name.pack()

    confirmBtn1.pack()
    confirmBtn2.pack()

    altContactFrame.grid( row = 0, column = 1 )

def createChatroom( name ):

    name = "chatroom__" + name

    try: os.mkdir( name )
    except: pass

    open(name + '/People.txt', 'w') if(not os.path.exists(name + '/People.txt')) else None
    open(name + '/Chats.txt', 'w') if(not os.path.exists(name + '/Chats.txt')) else None

    return None
    # return Chatroom.Chatroom( name )

def deleteChatroom( name ):

    name = "chatroom__" + name

    try:
        for fil in os.listdir(name): os.remove(name + '/' + fil)
        os.rmdir(name)
    except:
        pass

def selectChatroom( ):
    global mainWindow

def sendMsg( ):
    pass

def recvMsg( ):
    pass

print("-------------------------Starting App-------------------------")

# Loading contacts
UID = contacts.loadAll( )

# Creating window
mainWindow = getWindow( "Drocsid", "800x450" )
mainWindow.configure( bg = backgroundDefault )

# This is the part of the screen where you can click to add, remove, alter contacts and chatrooms
optionsFrame = tk.Frame( mainWindow )

# This is the frame for selecting the chatrooms
selectChatroomFrame = tk.Frame( mainWindow )

addContactBtn = tk.Button( master = optionsFrame, text = "Add Contact", font = ("Calibri", 16), command = addContact, bg = btnDefault, fg = btnTxtDefault )
remContactBtn = tk.Button( master = optionsFrame, text = "Remove Contact", font = ("Calibri", 16), command = remContact, bg = btnDefault, fg = btnTxtDefault )
altContactBtn = tk.Button( master = optionsFrame, text = "Edit Contact", font = ("Calibri", 16), command = altContact, bg = btnDefault, fg = btnTxtDefault )
selRoomBtn = tk.Button( master = optionsFrame, text = "Chats", font = ("Calibri", 16), command = selectChatroom, bg = btnDefault, fg = btnTxtDefault )

addContactBtn.config( height = 2, width = 20 )
remContactBtn.config( height = 2, width = 20 )
altContactBtn.config( height = 2, width = 20 )
selRoomBtn.config( height = 2, width = 20 )

addContactBtn.pack()
remContactBtn.pack()
altContactBtn.pack()
selRoomBtn.pack()

optionsFrame.grid( row = 0, column = 0 )

mainWindow.mainloop()

# saveContacts()
contacts.saveAll( )

print("-------------------------Closing App-------------------------")
#contacts_file.close()
