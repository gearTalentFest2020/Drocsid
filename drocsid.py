import tkinter as tk
import sys, os, socket
import contacts

from theme import *

contacts = contacts.contactsManager()

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

    promptWindow = getWindow( "Add Contact", "400x225" )

    name = tk.Entry( master = promptWindow)
    name.insert(string = "Name", index = 0)

    ip = tk.Entry( master = promptWindow)
    ip.insert(string = "IP", index = 0)

    ID = tk.Entry( master = promptWindow)
    ID.insert(string = "ID", index = 0)


    confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.addContact( ID.get(), name.get(), ip.get() ) or promptWindow.destroy() )

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

    confirmBtn = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.remContact(ID.get()) or promptWindow.destroy() )

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
    confirmBtn2 = tk.Button( master = promptWindow, text = "Submit", font = ("Calibri", 12), command = lambda : contacts.altContact( ID.get(), name.get(), ip.get() ) or promptWindow.destroy() )

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

print("-------------------------Starting App-------------------------")

# Loading contacts
contacts.loadAll( )

# Creating window
mainWindow = getWindow( "Drocsid", "800x450" )
mainWindow.configure( bg = backgroundDefault )

# This is the part of the screen where you can click to add, remove, alter contacts and chatrooms
optionsFrame = tk.Frame(mainWindow, bg = optBackgroundDefault )
#optionsFrame.grid( row = 0, column = 0, stick = "NW" )
optionsFrame.pack()


# These are the frames which replace the main screen upon selecting an option
addContactFrame = None
remContactFrame = None
AltContactFrame = None

# This is the frame for selecting the chatrooms
selectChatroomFrame = None

addContactBtn = getButton("Add Contact", command = addContact)
remContactBtn = getButton("Remove Contact", command = remContact)
altContactBtn = getButton("Edit Contact", command = altContact )
selRoomBtn = getButton("Select Chatroom", command = selectChatroom )

addContactBtn.pack()
remContactBtn.pack()
altContactBtn.pack()
selRoomBtn.pack()

mainWindow.mainloop()

# saveContacts()
contacts.saveAll( )

print("-------------------------Closing App-------------------------")
#contacts_file.close()