import os, sys, json
import socket, time, sqlite3
from baseChange import *

import hashlib
# import Client

class contactsManager:

    def __init__( self ):
        self.contacts = {}
        if(not os.path.exists('Contacts.txt')):
            f = open('Contacts.txt', 'w')
            f.write(self.generateUID()+'\n')
            f.close()

    def loadAll( self ):
        contacts_file = open('Contacts.txt', 'r')
        self.UID = None

        lines = contacts_file.readlines()
        self.UID = lines[0]

        for line in lines[1:]:
            tokens = line.split(';')
            tokens[1] = tokens[1][:-1]
            assert len(tokens)==2, "Corrupted Contacts File"
            self.contacts.setdefault(tokens[0], tokens[1])
        contacts_file.close()

        return self.UID.strip()

    def saveAll( self ):
        contacts_file = open('Contacts.txt', 'w')
        contacts_file.write(self.UID)
        for ID in self.contacts: contacts_file.write(ID + ";" + self.contacts[ID] + '\n')

    def addContact( self, ID, name):
        self.contacts.setdefault(ID.strip(), name.strip())

    def remContact( self, ID ):
        self.contacts.pop( ID.strip() )

    def altContact( self, ID, name):
        self.contacts[ID.strip()] = name.strip()

    def generateUID( self ):
        timestamp = str(int(time.time()))
        UID = convert(str(timestamp), 10, 64)[:-2]
        return UID

    def __getitem__( self, key ):
        return self.contacts.get(key, key)

class chatroomManager:
    target = "chats"

    def __init__( self ):
        self.rooms = []
        for i in os.listdir():
            if i.startswith("chatroom__"): self.rooms.append(i[10::])

    def addMemberTo( self, chatroom, UID ):
        fil = open('chatroom__'+chatroom+'/People.txt', 'r')
        members = [UID]
        lines = fil.readlines()
        for line in lines:
            line = line[:-1]
            members.append(line)
        fil.close()
        fil = open('chatroom__'+chatroom+'/People.txt', 'w')
        for member in members:
            fil.write(member + '\n')
        fil.close()

    def removeMemberFrom( self, chatroom, UID ):
        fil = open('chatroom__'+chatroom+'/People.txt', 'r')
        members = []
        lines = fil.readlines()
        for line in lines:
            line = line[:-1]
            if(line != UID): members.append(line)
        fil.close()
        fil = open('chatroom__'+chatroom+'/People.txt', 'w')
        for member in members:
            fil.write(member + '\n')
        fil.close()

    def addMsgTo( self, chatroom, key, sender , msg ):
        chatroom = 'chatroom__' + chatroom
        # This part of the code adds a msg (UID, timestamp, msg) to the DB of the correct chatroom
        name  =  chatroom + '/' + target + '.db'
        conn  =  sqlite3.connect( name )
        c = conn.cursor()
        try:
            ## Save string at new key location
            c.execute( '''INSERT INTO chat (time, sender, msg) VALUES (?,?,?)''', ( key, sender, msg ) )
            conn.commit()
        except Exception as e:
            pass
        conn.close()

    def getMsgsFrom( self, chatroom, n=50 ):
        # n is number of last chats to get
        chatroom = 'chatroom__' + chatroom
        name  =  chatroom + '/' + target + '.db'
        conn  =  sqlite3.connect( name )
        c = conn.cursor()
        c.execute('''SELECT time, sender, msg FROM chat''')
        l = c.fetchall()
        conn.commit()
        conn.close()
        return l[-1:-n-1:-1][::-1]

    def createRoom( self, name, members = [] ):

        self.rooms.append( name )

        chatroom = 'chatroom__' + name
        try: os.mkdir( chatroom )
        except: pass

        open(chatroom + '/People.txt', 'w') if(not os.path.exists(chatroom + '/People.txt')) else None
        for member in members:
            self.addMemberTo(name, member)

        target = 'chats'
        name  =  chatroom + '/' + target + '.db'
        conn  =  sqlite3.connect( name )
        c = conn.cursor()
        try:
            ## Create Table
            c.execute( '''CREATE TABLE chat(time REAL NOT NULL PRIMARY KEY, sender TEXT, msg TEXT)''' )
            conn.commit()

        except Exception as e:
            pass
        conn.close()

    def deleteRoom( self, chatroom ):
        self.rooms.remove( chatroom )
        chatroom = 'chatroom__' + chatroom
        try:
            for fil in os.listdir(chatroom): os.remove(chatroom + '/' + fil)
            os.rmdir(chatroom)
        except:
            pass

    def getMembersOf( self, chatroom ):
        chatroom = 'chatroom__' + chatroom
        fil = open(chatroom+'/People.txt', 'r')
        members = []
        lines = fil.readlines()
        for line in lines:
            line = line[:-1]
            members.append(line)
        fil.close()
        return members

    def getRooms( self ):
        return self.rooms