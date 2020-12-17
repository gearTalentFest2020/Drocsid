import tkinter as tk
import sys, os, socket
import Contacts
import Client
import time
import selectors

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

# ---------------------------------------------------------------------------------------------------- #

def createChatroom():
    CreateChatFrame = tk.Frame( master = chatwindow )

    createBtn['state'] = tk.DISABLED
    editBtn['state'] = tk.DISABLED
    deleteBtn['state'] = tk.DISABLED
    openBtn['state'] = tk.DISABLED

    def submit():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        uids = [i.strip() for i in people.get().split(',')]
        Client.createforothers(chatname, uids)
        uids.append(Client.myUID)
        queryList.append(['create', chatname, uids])
        CreateChatFrame.destroy()

    def back():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL
        CreateChatFrame.destroy()


    name = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    people = tk.Entry(master=CreateChatFrame, font=("Calibri", 16))
    people.insert(string="Enter UIDs of the people (comma seperated)", index=0)

    confirmBtn = tk.Button(master=CreateChatFrame, text="Submit", font=("Calibri", 16), command= submit, fg="#008000")
    backBtn = tk.Button(master=CreateChatFrame, text="Cancel", font=("Calibri", 16), command = back)

    CreateChatFrame.grid(rowspan = 3,column=1)
    name.pack()
    people.pack()
    confirmBtn.pack()
    backBtn.pack()

def deleteChatroom():
    DeleteChatFrame = tk.Frame(master = chatwindow)

    createBtn['state'] = tk.DISABLED
    editBtn['state'] = tk.DISABLED
    deleteBtn['state'] = tk.DISABLED
    openBtn['state'] = tk.DISABLED

    def Delete( ):
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        Client.remove(chatname, chatsManager.getMembersOf(chatname))
        queryList.append(['delete', chatname])
        DeleteChatFrame.destroy()

    def back():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL
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
    
    createBtn['state'] = tk.DISABLED
    editBtn['state'] = tk.DISABLED
    deleteBtn['state'] = tk.DISABLED
    openBtn['state'] = tk.DISABLED


    def Edit():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL

        chatname = name.get().strip()
        UID_add = peopleadd.get().strip()
        Client.add(chatname, chatsManager.getMembersOf(chatname), UID_add)
        queryList.append(['add', chatname, UID_add])
        EditChatFrame.destroy()

    def back():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL
        EditChatFrame.destroy()

    name = tk.Entry(master=EditChatFrame, font=("Calibri", 16))
    name.insert(string="Enter Chatroom name", index=0)

    peopleadd = tk.Entry(master=EditChatFrame, font=("Calibri", 16), width=36)
    peopleadd.insert(string="Enter UID of the person you want to add", index=0)


    confirmBtn = tk.Button(master=EditChatFrame, text="Submit", font=("Calibri", 16), command=Edit,fg="#008000")
    backBtn = tk.Button(master=EditChatFrame, text="Cancel", font=("Calibri", 16), command=back)

    EditChatFrame.grid(rowspan=3, column=1)
    name.pack(fill = tk.X)

    peopleadd.pack()
    confirmBtn.pack()
    backBtn.pack()

def openChatroom():
    OpenChatFrame = tk.Frame(master = chatwindow)
    
    createBtn['state'] = tk.DISABLED
    editBtn['state'] = tk.DISABLED
    deleteBtn['state'] = tk.DISABLED
    openBtn['state'] = tk.DISABLED

    def back():
        createBtn['state'] = tk.NORMAL
        editBtn['state'] = tk.NORMAL
        deleteBtn['state'] = tk.NORMAL
        openBtn['state'] = tk.NORMAL
        OpenChatFrame.destroy()

    chatnames = chatsManager.getRooms()

    for i in chatnames:
        btn = tk.Button(master = OpenChatFrame, text = i, font=("Calibri", 16), bg = "#ffffff", command = lambda i=i: chatMainWindow(i))
        btn.pack(fill = tk.X)

    backBtn = tk.Button(master=OpenChatFrame, text="Cancel", font=("Calibri", 16), command=back)

    OpenChatFrame.grid(rowspan = 3, column = 1)
    backBtn.pack(fill = tk.X)

def chatMainWindow(chatname):
    Window = tk.Tk()

    createBtn['state'] = tk.NORMAL
    editBtn['state'] = tk.NORMAL
    deleteBtn['state'] = tk.NORMAL
    openBtn['state'] = tk.NORMAL


    def layout(name):

        Window.title("Drocsid")
        Window.configure(width = 450, height = 800, bg = "#17202A")

        labelHead = tk.Label(Window, bg = "#17202A", fg = "#EAECEE", text = name , font = "Helvetica 13 bold", pady = 5)
        labelHead.place(relwidth = 1)
        line = tk.Label(Window, width = 450, bg = "#ABB2B9")
        line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        tup_msgs = [("12:00", "Chow", "Hello"), ("12:01", "Vyoman", "Hi"), ("12:02", "Aryan", "Bye"), ("12:03", "Agarwal", "Goodbye"),("12:00", "Chow", "Hello"), ("12:01", "Vyoman", "Hi"), ("12:02", "Aryan", "Bye"), ("12:03", "Agarwal", "Goodbye"),("12:00", "Chow", "Hello"), ("12:01", "Vyoman", "Hi"), ("12:02", "Aryan", "Bye"), ("12:03", "Agarwal", "Goodbye")]
        msg = ""
        for i in tup_msgs:
            msg += i[0] + "\t" + i[1] + "\n" + i[2]+"\n\n"
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

        # create a scroll bar
        scrollbar = tk.Scrollbar(textCons)
        # place the scroll bar into the GUI window
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = textCons.yview)
        textCons.config(state = tk.DISABLED)

    # function to basically start the thread for sending messages
    def sendButton():
        msg = entryMsg.get()
        timestamp = time.time()
        Client.send(chatname,chatsManager.getMembersOf(chatname),timestamp,msg)
        queryList.append(['recv', chatname, timestamp, UID,  msg])

    def printMsg():
        textCons.insert(0,chatmsg)





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
UID = contacts.loadAll( ) #Print it
Client.myUID = UID
Client.connect()
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


while True:
    queryList += Client.recv()

    for query in queryList:
        print(query)
        if(query[0] == 'create'):
            chatsManager.createRoom( query[1], query[2] )
        elif(query[0] == 'delete'):
            chatsManager.deleteRoom( query[1] )
        elif(query[0] == 'add'):
            chatsManager.addMemberTo( query[1], query[2] )
        elif(query[0] == 'remove'):
            try:
                chatsManager.removeMemberFrom( query[1], query[2] )
            except:
                pass
        elif(query[0] == 'addmsg'):
            chatsManager.addMsgTo(query[1],query[2],query[3],query[4])

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

# saveContacts()
contacts.saveAll( )
Client.stop()
print("-------------------------Closing App-------------------------")
