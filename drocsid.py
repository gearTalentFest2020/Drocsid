import tkinter as tk
import sys, os, socket, time
import Contacts, Client

from theme import *

contacts = Contacts.contactsManager()
chatsManager = Contacts.chatroomManager()
chatsEnabled = False
queryList = []

# Wrapper around windows
def getWindow( title, geometry ):
    temp = tk.Tk()
    temp.title( title )
    temp.geometry( geometry )
    return temp

def setNormal( *args ):
    for button in args: button['state'] = tk.NORMAL

def setDisabled( *args ):
    for button in args: button['state'] = tk.DISABLED

# Function to add a contact
def addContact( ):

    def back():
        addContactFrame.destroy()
        setNormal(remContactBtn, altContactBtn)
        # remContactBtn["state"] = tk.NORMAL
        # altContactBtn["state"] = tk.NORMAL

    setDisabled(remContactBtn, altContactBtn)
    # remContactBtn["state"] = tk.DISABLED
    # altContactBtn["state"] = tk.DISABLED

    addContactFrame = tk.Frame( master = mainWindow )

    name = tk.Entry( master = addContactFrame, font = ("Calibri", 16))
    name.insert(string = "Enter contact's name", index = 0)

    ID = tk.Entry( master = addContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = addContactFrame, text = "Submit", font = ("Calibri", 16), command = lambda : contacts.addContact(ID.get().strip(), name.get().strip()) or back(), fg = "#008000")
    backBtn = tk.Button(master = addContactFrame, text = "Cancel", font = ("Calibri", 16), command = back)

    name.pack()
    ID.pack()

    confirmBtn.pack(fill = tk.X)
    backBtn.pack(fill = tk.X)
    addContactFrame.grid( row = 1, column = 1, sticky = tk.E )

# Function to remove a contact
def remContact( ):

    def back():
        remContactFrame.destroy()
        setNormal( addContactBtn, altContactBtn )
        # addContactBtn["state"] = tk.NORMAL
        # altContactBtn["state"] = tk.NORMAL

    setDisabled( addContactBtn, altContactBtn )
    # addContactBtn["state"] = tk.DISABLED
    # altContactBtn["state"] = tk.DISABLED

    remContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = remContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    confirmBtn = tk.Button( master = remContactFrame, text = "Remove", font = ("Calibri", 16), command = lambda : contacts.remContact(ID.get()) or back(), fg = "#008000")
    backBtn = tk.Button(master = remContactFrame, text = "Cancel", font = ("Calibri", 16), command = back)

    ID.pack()

    confirmBtn.pack(fill = tk.X)
    backBtn.pack(fill = tk.X)

    remContactFrame.grid( row = 1, column = 1, sticky = tk.E  )

# Function to alter a contact
def altContact( ):

    def back():
        altContactFrame.destroy()
        setNormal( addContactBtn, remContactBtn )
        # addContactBtn["state"] = tk.NORMAL
        # remContactBtn["state"] = tk.NORMAL

    setDisabled( addContactBtn, remContactBtn )
    # addContactBtn["state"] = tk.DISABLED
    # remContactBtn["state"] = tk.DISABLED

    altContactFrame = tk.Frame( master = mainWindow )

    ID = tk.Entry( master = altContactFrame, font = ("Calibri", 16))
    ID.insert(string = "Enter contact's ID", index = 0)

    name = tk.Entry( master = altContactFrame, font = ("Calibri", 16))

    confirmBtn1 = tk.Button( master = altContactFrame, text = "Edit", font = ("Calibri", 16), command = lambda : name.insert(string = contacts[ID.get().strip()], index = 0), fg = "#008000")
    confirmBtn2 = tk.Button( master = altContactFrame, text = "Submit", font = ("Calibri", 16), command = lambda : contacts.altContact(ID.get(), name.get()) or back(), fg = "#008000")
    backBtn = tk.Button(master = altContactFrame, text = "Cancel", font = ("Calibri", 16), command = back)

    ID.pack()
    name.pack()

    confirmBtn1.pack()
    confirmBtn2.pack()
    backBtn.pack()

    altContactFrame.grid( row = 1, column = 1 , sticky = tk.E )

# ---------------------------------------------------------------------------------------------------- #

def createChatroom():
    CreateChatFrame = tk.Frame( master = chatwindow )

    def submit():
        setNormal(createBtn, editBtn, deleteBtn, openBtn)
        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        Client.myUIDs = [i.strip() for i in people.get().split(',')]
        Client.createforothers(chatname, Client.myUIDs)
        Client.myUIDs.append(Client.myUID)
        queryList.append(['create', chatname, Client.myUIDs])
        CreateChatFrame.destroy()

    def back():
        setNormal(createBtn, editBtn, deleteBtn, openBtn)
        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL
        CreateChatFrame.destroy()

    setDisabled(createBtn, editBtn, deleteBtn, openBtn)

    # createBtn['state'] = tk.DISABLED
    # editBtn['state'] = tk.DISABLED
    # deleteBtn['state'] = tk.DISABLED
    # openBtn['state'] = tk.DISABLED

    name = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    people = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    people.insert(string="Enter Client.myUIDs of the people (comma seperated)", index=0)

    confirmBtn = tk.Button(master=CreateChatFrame, text="Submit", font=("Calibri", 16), command= submit, fg="#008000")
    backBtn = tk.Button(master=CreateChatFrame, text="Cancel", font=("Calibri", 16), command = back)

    CreateChatFrame.grid(rowspan = 3,column=1)
    name.pack()
    people.pack()
    confirmBtn.pack()
    backBtn.pack()

def deleteChatroom():
    DeleteChatFrame = tk.Frame(master = chatwindow)

    setDisabled(createBtn, editBtn, deleteBtn, openBtn)

    # createBtn['state'] = tk.DISABLED
    # editBtn['state'] = tk.DISABLED
    # deleteBtn['state'] = tk.DISABLED
    # openBtn['state'] = tk.DISABLED

    def Delete( ):

        setNormal(createBtn, editBtn, deleteBtn, openBtn)

        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        members = chatsManager.getMembersOf(chatname)
        members.remove(Client.myUID)
        Client.remove(chatname, members)
        queryList.append(['delete', chatname])
        DeleteChatFrame.destroy()

    def back():

        setNormal(createBtn, editBtn, deleteBtn, openBtn)

        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL
        DeleteChatFrame.destroy()

    name = tk.Entry(master=DeleteChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    confirmBtn = tk.Button(master=DeleteChatFrame, text="Submit", font=("Calibri", 16),command = Delete, fg="#008000")
    backBtn = tk.Button(master=DeleteChatFrame, text="Cancel", font=("Calibri", 16), command=back)

    DeleteChatFrame.grid(rowspan = 3,column=1)
    name.pack()
    confirmBtn.pack()
    backBtn.pack()

def editChatroom():
    EditChatFrame = tk.Frame(master=chatwindow)

    def Edit():

        setNormal(createBtn, editBtn, deleteBtn, openBtn)

        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        Client.myUID_add = peopleadd.get().strip()
        Client.add(chatname, chatsManager.getMembersOf(chatname), Client.myUID_add)
        queryList.append(['addper', chatname, Client.myUID_add])
        EditChatFrame.destroy()

    def back():

        setNormal(createBtn, editBtn, deleteBtn, openBtn)

        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL
        EditChatFrame.destroy()

    setDisabled(createBtn, editBtn, deleteBtn, openBtn)

    # createBtn['state'] = tk.DISABLED
    # editBtn['state'] = tk.DISABLED
    # deleteBtn['state'] = tk.DISABLED
    # openBtn['state'] = tk.DISABLED

    name = tk.Entry(master=EditChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    peopleadd = tk.Entry(master=EditChatFrame, font=("Calibri", 16), width=36)
    peopleadd.insert(string="Enter Client.myUID of the person you want to add", index=0)


    confirmBtn = tk.Button(master=EditChatFrame, text="Submit", font=("Calibri", 16), command=Edit,fg="#008000")
    backBtn = tk.Button(master=EditChatFrame, text="Cancel", font=("Calibri", 16), command=back)

    EditChatFrame.grid(rowspan=3, column=1)
    name.pack(fill = tk.X)

    peopleadd.pack()
    confirmBtn.pack()
    backBtn.pack()

def openChatroom():
    OpenChatFrame = tk.Frame(master = chatwindow)

    def back():

        setNormal(createBtn, editBtn, deleteBtn, openBtn)
        # createBtn['state'] = tk.NORMAL
        # editBtn['state'] = tk.NORMAL
        # deleteBtn['state'] = tk.NORMAL
        # openBtn['state'] = tk.NORMAL
        OpenChatFrame.destroy()

    setDisabled(createBtn, editBtn, deleteBtn, openBtn)

    # createBtn['state'] = tk.DISABLED
    # editBtn['state'] = tk.DISABLED
    # deleteBtn['state'] = tk.DISABLED
    # openBtn['state'] = tk.DISABLED

    chatnames = chatsManager.getRooms()

    for i in chatnames:
        btn = tk.Button(master = OpenChatFrame, text = i, font=("Calibri", 16), bg = "#ffffff", command = lambda i=i: chatMainWindow(i))
        btn.pack(fill = tk.X)

    backBtn = tk.Button(master=OpenChatFrame, text="Cancel", font=("Calibri", 16), command=back)

    OpenChatFrame.grid(rowspan = 3, column = 1)
    backBtn.pack(fill = tk.X)

def chatMainWindow(chatname):
    Window = getWindow("Drocsid", "450x800")

    setNormal(createBtn, editBtn, deleteBtn, openBtn)

    # createBtn['state'] = tk.NORMAL
    # editBtn['state'] = tk.NORMAL
    # deleteBtn['state'] = tk.NORMAL
    # openBtn['state'] = tk.NORMAL

    currentlyOpenChat = chatname

    def layout(name):

        Window.configure( bg = "#17202A" )

        labelHead = tk.Label(Window, bg = "#17202A", fg = "#EAECEE", text = name , font = "Helvetica 13 bold", pady = 5)
        labelHead.place(relwidth = 1)
        line = tk.Label(Window, width = 450, bg = "#ABB2B9")
        line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        tup_msgs = chatsManager.getMsgsFrom(chatname)
        msg = ""
        for i in tup_msgs:
            msg += str(i[0]) + "\t" + contacts[i[1]] + "\n" + i[2]+"\n\n"
        print(msg)


        global textCons
        textCons = tk.Text(Window, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5)
        textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        textCons.insert(tk.END,msg)

        labelBottom = tk.Label(Window, bg = "#ABB2B9", height = 80)
        labelBottom.place(relwidth = 1, rely = 0.825)

        global entryMsg
        entryMsg = tk.Entry(labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")

        # place the given widget
        # into the gui window
        entryMsg.place(relwidth = 0.74,relheight = 0.06, rely = 0.008, relx = 0.011)
        entryMsg.focus()

        # create a Send Button
        buttonMsg = tk.Button(labelBottom, text = "Send", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = sendButton)
        buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)
        textCons.config(cursor = "arrow")

        reloadButton = tk.Button(labelBottom, text="Reload", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = lambda : chatMainWindow(chatname) or Window.destroy())

        # create a scroll bar
        scrollbar = tk.Scrollbar(textCons)
        # place the scroll bar into the GUI window
        scrollbar.place(relheight = 1, relx = 0.974)
        reloadButton.place(rely = 0.05, relx = 0.011)
        scrollbar.config(command = textCons.yview)
        textCons.config(state = tk.DISABLED)

    # function to basically start the thread for sending messages
    def sendButton():
        msg = entryMsg.get()
        timestamp = time.time()
        Client.send(chatname,chatsManager.getMembersOf(chatname),timestamp,msg)
        queryList.append(['addmsg', chatname, timestamp, Client.myUID,  msg])

    layout(chatname)

def selectChatroom():
    global mainWindow, chatwindow
    global createBtn, editBtn, deleteBtn, openBtn

    chatwindow = getWindow("Chats", geometry="800x450")
    chatwindow.config(bg=backgroundDefault)

    createBtn = tk.Button(master=chatwindow, text="Create chatroom", font=("Calibri", 16), height=1, width=20,bg="#ffffff", command=createChatroom)
    editBtn = tk.Button(master=chatwindow, text="Edit chatroom", font=("Calibri", 16), height=1, width=20, bg="#ffffff",command=editChatroom)
    deleteBtn = tk.Button(master=chatwindow, text="Delete chatroom", font=("Calibri", 16), height=1, width=20,bg="#ffffff", command=deleteChatroom)
    openBtn = tk.Button(master=chatwindow, text="Open chatroom", font=("Calibri", 16), height=1, width=20, bg="#ffffff",command=openChatroom)

    createBtn.grid(row=0, column=0)
    editBtn.grid(row=1, column=0)
    deleteBtn.grid(row=2, column=0)
    openBtn.grid(row=3, column=0)

    chatsEnabled = True

print("-------------------------Starting App-------------------------")

# Loading contacts
Client.myUID = contacts.loadAll( ) #Print it
Client.connect()

# Creating window
mainWindow = getWindow( "Drocsid","800x450" )
mainWindow.configure( bg = backgroundDefault )

# This is the part of the screen where you can click to add, remove, alter contacts and chatrooms
optionsFrame = tk.Frame( mainWindow )

# This is the frame for selecting the chatrooms
selectChatroomFrame = tk.Frame( mainWindow )

Title = tk.Label(master = mainWindow, text= "DROCSID", font = ("Calibri", 30),bg = backgroundDefault, fg = "#ffffff")

addContactBtn = tk.Button( master = optionsFrame, text = "Add Contact", font = ("Consolas", 20), command = addContact, bg = btnDefault, fg = btnTxtDefault )
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

while True:
    queryList += Client.recv()

    for query in queryList:
        print(query)
        name = query[1]
        if(query[0] == 'create'):
            chatsManager.createRoom( query[1], query[2] )
        elif(query[0] == 'addmsg'):
            chatsManager.addMsgTo( query[1],query[2],query[3],query[4] )
        elif(query[0] == 'addper'):
            chatsManager.addMemberTo( query[1], query[2] )
        elif(query[0] == 'remper'):
            if(query[2] == Client.myUID): chatsManager.deleteRoom( query[1] )
            else: chatsManager.removeMemberFrom( query[1], query[2] )

    queryList = []

    try:
        mainWindow.update_idletasks()
        mainWindow.update()
    except Exception as e:
        break

    if chatsEnabled:
        try:
            chatwindow.update_idletasks()
            chatwindow.update()
        except:
            chatsEnabled = False

contacts.saveAll( )
Client.stop()

print("-------------------------Closing App-------------------------")
