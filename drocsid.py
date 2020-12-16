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

    def Close_Add():
        contacts.addContact(ID.get(), name.get())
        addContactFrame.destroy()
        remContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    remContactBtn["state"] = tk.DISABLED
    altContactBtn["state"] = tk.DISABLED

    addContactFrame = tk.Frame( master = mainWindow )

    name = tk.Entry( master = addContactFrame)
    name.insert(string = "Enter contact's name", index = 0)

    ID = tk.Entry( master = addContactFrame)
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = addContactFrame, text = "Submit", font = ("Calibri", 12), command = Close_Add)

    name.pack()
    ID.pack()

    confirmBtn.pack()
    addContactFrame.grid( row = 2, column = 1, sticky = tk.S )

# Function to remove a contact
def remContact( ):

    def Close_Rem():
        contacts.remContact(ID.get())
        remContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    addContactBtn["state"] = tk.DISABLED
    altContactBtn["state"] = tk.DISABLED

    remContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = remContactFrame)
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = remContactFrame, text = "Remove", font = ("Calibri", 12), command = Close_Rem)

    ID.pack()
    confirmBtn.pack()

    remContactFrame.grid( row = 2, column = 1, sticky = tk.S  )

# Function to alter a contact
def altContact( ):

    def Close_Alt():
        contacts.altContact(ID.get(), name.get())
        altContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        remContactBtn["state"] = tk.NORMAL

    addContactBtn["state"] = tk.DISABLED
    remContactBtn["state"] = tk.DISABLED

    altContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = altContactFrame )
    ID.insert(string = "Enter contact's ID", index = 0)

    name = tk.Entry( master = altContactFrame )

    confirmBtn1 = tk.Button( master = altContactFrame, text = "Edit", font = ("Calibri", 12), command = lambda : name.insert(string = contacts[ID.get().strip()], index = 0))
    confirmBtn2 = tk.Button( master = altContactFrame, text = "Submit", font = ("Calibri", 12), command = Close_Alt)

    ID.pack()
    name.pack()

    confirmBtn1.pack()
    confirmBtn2.pack()

    altContactFrame.grid( row = 2, column = 1 , sticky = tk.S )

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
mainWindow = getWindow("Drocsid","800x450")
mainWindow.attributes("-fullscreen",True)
mainWindow.configure( bg = backgroundDefault )

# This is the part of the screen where you can click to add, remove, alter contacts and chatrooms
optionsFrame = tk.Frame( mainWindow )

# This is the frame for selecting the chatrooms
selectChatroomFrame = tk.Frame( mainWindow )

Title = tk.Label(master = mainWindow, text= "DROCSID", font = ("Calibri", 24),bg = backgroundDefault, fg = "#ffffff")


addContactBtn = tk.Button( master = optionsFrame, text = "Add Contact", font = ("Calibri", 16), command = addContact, bg = btnDefault, fg = btnTxtDefault )
remContactBtn = tk.Button( master = optionsFrame, text = "Remove Contact", font = ("Calibri", 16), command = remContact, bg = btnDefault, fg = btnTxtDefault )
altContactBtn = tk.Button( master = optionsFrame, text = "Edit Contact", font = ("Calibri", 16), command = altContact, bg = btnDefault, fg = btnTxtDefault )
selRoomBtn = tk.Button( master = optionsFrame, text = "Chats", font = ("Calibri", 16), command = selectChatroom, bg = btnDefault, fg = btnTxtDefault )
exitBtn = tk.Button( master = optionsFrame, text = "Exit", font = ("Calibri", 12), command = mainWindow.destroy, bg = "#ff0000", fg = btnTxtDefault )

addContactBtn.config( height = 2, width = 20 )
remContactBtn.config( height = 2, width = 20 )
altContactBtn.config( height = 2, width = 20 )
selRoomBtn.config( height = 2, width = 20 )

Title.grid(row = 0,column = 0)
addContactBtn.pack()
remContactBtn.pack()
altContactBtn.pack()
selRoomBtn.pack()
exitBtn.pack(fill = tk.X)
optionsFrame.grid( row = 1, column = 0 )

mainWindow.mainloop()

# saveContacts()
contacts.saveAll( )

print("-------------------------Closing App-------------------------")
#contacts_file.close()
