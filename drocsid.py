import tkinter as tk
import sys, os, socket
import Contacts
import Client

import selectors

from theme import *

contacts = Contacts.contactsManager()
queryList = []
['create', nameofroom, ]
where do i put createdb
# Wrapper around windows
def getWindow( title, geometry ):
    temp = tk.Tk()
    temp.title( title )
    temp.geometry( geometry )
    return temp

# Function to add a contact
def addContact( ):

    def Close_Add():
        contacts.addContact(ID.get(), name.get())
        addContactFrame.destroy()
        remContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    def Back_Add():
        addContactFrame.destroy()
        remContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    remContactBtn["state"] = tk.DISABLED
    altContactBtn["state"] = tk.DISABLED

    addContactFrame = tk.Frame( master = mainWindow)

    name = tk.Entry( master = addContactFrame, font = ("Calibri", 16))
    name.insert(string = "Enter contact's name", index = 0)

    ID = tk.Entry( master = addContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = addContactFrame, text = "Submit", font = ("Calibri", 16), command = Close_Add, fg = "#008000")
    backBtn = tk.Button(master = addContactFrame, text = "Cancel", font = ("Calibri", 16), command = Back_Add)

    name.pack()
    ID.pack()

    confirmBtn.pack(fill = tk.X)
    backBtn.pack(fill = tk.X)
    addContactFrame.grid( row = 1, column = 1, sticky = tk.E )

# Function to remove a contact
def remContact( ):

    def Close_Rem():
        contacts.remContact(ID.get())
        remContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    def Back_Rem():
        remContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        altContactBtn["state"] = tk.NORMAL

    addContactBtn["state"] = tk.DISABLED
    altContactBtn["state"] = tk.DISABLED

    remContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = remContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = remContactFrame, text = "Remove", font = ("Calibri", 16), command = Close_Rem, fg = "#008000")
    backBtn = tk.Button(master = remContactFrame, text = "Cancel", font = ("Calibri", 16), command = Back_Rem)

    ID.pack()

    confirmBtn.pack(fill = tk.X)
    backBtn.pack(fill = tk.X)

    remContactFrame.grid( row = 1, column = 1, sticky = tk.E  )

# Function to alter a contact
def altContact( ):

    def Close_Alt():
        contacts.altContact(ID.get(), name.get())
        altContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        remContactBtn["state"] = tk.NORMAL

    def Back_Alt():
        altContactFrame.destroy()
        addContactBtn["state"] = tk.NORMAL
        remContactBtn["state"] = tk.NORMAL

    addContactBtn["state"] = tk.DISABLED
    remContactBtn["state"] = tk.DISABLED

    altContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = altContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    name = tk.Entry( master = altContactFrame, font = ("Calibri", 16))

    confirmBtn1 = tk.Button( master = altContactFrame, text = "Edit", font = ("Calibri", 16), command = lambda : name.insert(string = contacts[ID.get().strip()], index = 0), fg = "#008000")
    confirmBtn2 = tk.Button( master = altContactFrame, text = "Submit", font = ("Calibri", 16), command = Close_Alt, fg = "#008000")
    backBtn = tk.Button(master = altContactFrame, text = "Cancel", font = ("Calibri", 16), command = Back_Alt)


    ID.pack()
    name.pack()

    confirmBtn1.pack()
    confirmBtn2.pack()
    backBtn.pack()

    altContactFrame.grid( row = 1, column = 1 , sticky = tk.E )

def createChatroom():
    CreateChatFrame = tk.Frame(master=chatwindow)

    name = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)
    chatname = name.get()

    people = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    people.insert(string="Enter UIDs of the people you wish to chat with", index=0)

    confirmBtn = tk.Button(master=CreateChatFrame, text="Submit", font=("Calibri", 16), command= lambda:Client.create(name.get()) or CreateChatFrame.destroy, fg="#008000")
    backBtn = tk.Button(master=CreateChatFrame, text="Cancel", font=("Calibri", 16), command = CreateChatFrame.destroy)

    CreateChatFrame.grid(rowspan = 3,column=1)
    name.pack()
    people.pack()
    confirmBtn.pack()
    backBtn.pack()

    chatname = "chatroom__" + chatname

    try: os.mkdir( chatname )
    except: pass

    open(chatname + '/People.txt', 'w') if(not os.path.exists(chatname + '/People.txt')) else None
    Client.create(chatname)


def deleteChatroom():
    def Delete(chatname):
        chatname = "chatroom__" + chatname

        try:
            for fil in os.listdir(chatname): os.remove(chatname + '/' + fil)
            os.rmdir(chatname)
        except:
            pass

        DeleteChatFrame.destroy
    
    DeleteChatFrame = tk.Frame(master = chatwindow)
    name = tk.Entry(master=DeleteChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    chatname = name.get()

    confirmBtn = tk.Button(master=DeleteChatFrame, text="Submit", font=("Calibri", 16),command = Delete(chatname), fg="#008000")
    backBtn = tk.Button(master=DeleteChatFrame, text="Cancel", font=("Calibri", 16), command=DeleteChatFrame.destroy)

    DeleteChatFrame.grid(rowspan = 3,column=1)
    name.pack()
    confirmBtn.pack()
    backBtn.pack()

def editChatroom():
    def Delete(chatname):
        chatname = "chatroom__" + chatname

        try:
            for fil in os.listdir(chatname): os.remove(chatname + '/' + fil)
            os.rmdir(chatname)
        except:
            pass

        EditChatFrame.destroy

    EditChatFrame = tk.Frame(master=chatwindow)

    name = tk.Entry(master=EditChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    peoplermv = tk.Entry(master=EditChatFrame, font=("Calibri", 16), width= 36)
    peoplermv.insert(string="Enter UIDs of the people you want to remove(type 0 for none)", index=0)

    peopleadd = tk.Entry(master=EditChatFrame, font=("Calibri", 16), width=36)
    peopleadd.insert(string="Enter UIDs of the people you want to add(type 0 for none)", index=0)

    chatname = name.get()

    confirmBtn = tk.Button(master=EditChatFrame, text="Submit", font=("Calibri", 16), command=Delete(chatname),fg="#008000")
    backBtn = tk.Button(master=EditChatFrame, text="Cancel", font=("Calibri", 16), command=EditChatFrame.destroy)

    EditChatFrame.grid(rowspan=3, column=1)
    name.pack(fill = tk.X)
    peoplermv.pack()
    peopleadd.pack()
    confirmBtn.pack()
    backBtn.pack()

def openChatroom():
    pass

def selectChatroom():
    global mainWindow, chatwindow


    chatwindow = getWindow("Chats", geometry="800x450")
    chatwindow.config(bg=backgroundDefault)

    createBtn = tk.Button(master=chatwindow, text="Create new chatroom", font=("Calibri", 16), height=1, width=20,bg="#ffffff", command=createChatroom)
    editBtn = tk.Button(master=chatwindow, text="Edit chatroom", font=("Calibri", 16), height=1, width=20, bg="#ffffff",command=editChatroom)
    deleteBtn = tk.Button(master=chatwindow, text="Delete chatroom", font=("Calibri", 16), height=1, width=20,bg="#ffffff", command=deleteChatroom)
    openBtn = tk.Button(master=chatwindow, text="Open chatroom", font=("Calibri", 16), height=1, width=20, bg="#ffffff",command=openChatroom)


    createBtn.grid(row=0, column=0)
    editBtn.grid(row=1, column=0)
    deleteBtn.grid(row=2, column=0)
    openBtn.grid(row=3, column=0)


    chatwindow.mainloop()


def sendMsg( ):
    pass

def recvMsg( ):
    pass

print("-------------------------Starting App-------------------------")

# Loading contacts
UID = contacts.loadAll( )

# Creating window
mainWindow = getWindow("Drocsid","800x450")
mainWindow.configure( bg = backgroundDefault )

# This is the part of the screen where you can click to add, remove, alter contacts and chatrooms
optionsFrame = tk.Frame( mainWindow )

# This is the frame for selecting the chatrooms
selectChatroomFrame = tk.Frame( mainWindow )

Title = tk.Label(master = mainWindow, text= "DROCSID", font = ("Calibri", 30),bg = backgroundDefault, fg = "#ffffff")


addContactBtn = tk.Button( master = optionsFrame, text = "Add Contact", font = ("Calibri", 20), command = addContact, bg = btnDefault, fg = btnTxtDefault )
remContactBtn = tk.Button( master = optionsFrame, text = "Remove Contact", font = ("Calibri", 20), command = remContact, bg = btnDefault, fg = btnTxtDefault )
altContactBtn = tk.Button( master = optionsFrame, text = "Edit Contact", font = ("Calibri", 20), command = altContact, bg = btnDefault, fg = btnTxtDefault )
selRoomBtn = tk.Button( master = optionsFrame, text = "Chats", font = ("Calibri", 20), command = selectChatroom, bg = btnDefault, fg = btnTxtDefault )

addContactBtn.config( height = 2, width = 20 )
remContactBtn.config( height = 2, width = 20 )
altContactBtn.config( height = 2, width = 20 )
selRoomBtn.config( height = 2, width = 20 )

Title.grid(row = 0,column = 0)
addContactBtn.pack()
remContactBtn.pack()
altContactBtn.pack()
selRoomBtn.pack()
optionsFrame.grid( row = 1, column = 0 )

Client.UID = UID
while True:
    clientList = Client.recv()
    for q in clientList: queryList.append(q)
    try:
        mainWindow.update_idletasks()
        mainWindow.update()
    except Exception as e:
        break

# saveContacts()
contacts.saveAll( )

print("-------------------------Closing App-------------------------")
