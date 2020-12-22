import os, sys, json
import socket, time, sqlite3
from baseChange import *

class contactsManager:

    def __init__( self ):

        self.contacts = {}
        self.names = {}

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
            line = line[:-1]
            tokens = line.split(';')
            assert len(tokens)==2, "Corrupted Contacts File"
            self.contacts.setdefault(tokens[0], tokens[1])
            self.names.setdefault(tokens[1], tokens[0])
        contacts_file.close()

        return self.UID.strip()

    def saveAll( self ):
        contacts_file = open('Contacts.txt', 'w')
        contacts_file.write(self.UID)
        for ID in self.contacts: contacts_file.write(ID + ";" + self.contacts[ID] + '\n')

    def addContact( self, ID, name):

        ID = ID.strip()
        name = name.strip()

        self.contacts.setdefault( ID, name )
        self.names.setdefault( name, ID )

    def remContact( self, ID ):

        ID = ID.strip()

        self.names.pop( self.contacts[ID] )
        self.contacts.pop( ID )

    def altContact( self, ID, name ):

        ID = ID.strip()
        name = name.strip()

        oldName = self.contacts[ID]
        self.contacts[ID] = name
        self.names.pop(oldName)
        self.names[name] = ID

    def generateUID( self ):
        timestamp = str(int(time.time()))
        UID = convert(str(timestamp), 10, 64)[:-2]
        return UID

    def __getitem__( self, key ):
        return self.contacts.get(key, key)

    def getName( self, key ):
        return self.contacts.get(key, key)

    def getUID( self, key ):
        return self.names.get(key, '')

class chatroomManager:

    def __init__( self ):
        self.rooms = []
        for entry in os.listdir():
            if entry.startswith("chatroom__"): self.rooms.append(entry[10::])

    def addMemberTo( self, name, UID ):

        chatroom = 'chatroom__' + name
        members = [UID]

        fil = open(chatroom+'/People.txt', 'r')
        lines = fil.readlines()
        for line in lines: members.append(line[:-1])
        fil.close()

        fil = open(chatroom+'/People.txt', 'w')
        for member in members: fil.write(member + '\n')
        fil.close()

    def removeMemberFrom( self, name, toRem ):

        chatroom = 'chatroom__' + name
        fil = open(chatroom+'/People.txt', 'r')
        members = []
        lines = fil.readlines()

        for line in lines:
            line = line[:-1]
            if(line != toRem): members.append(line)
        fil.close()

        fil = open(chatroom+'/People.txt', 'w')
        for member in members: fil.write(member + '\n')
        fil.close()

    def addMsgTo( self, name, key, sender , msg ):
        chatroom = 'chatroom__' + name
        # This part of the code adds a msg (UID, timestamp, msg) to the DB of the correct chatroom
        name  =  chatroom + '/chats.db'
        conn  =  sqlite3.connect( name )
        c = conn.cursor()
        try:
            c.execute( '''INSERT INTO chat (time, sender, msg) VALUES (?,?,?)''', ( key, sender, msg ) )
            conn.commit()
        except Exception as e:
            pass
        conn.close()

    def getMsgsFrom( self, name, n = 64 ):

        chatroom = 'chatroom__' + name
        name  =  chatroom + '/chats.db'
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

        name  =  chatroom + '/chats.db'
        conn  =  sqlite3.connect( name )
        c = conn.cursor()
        try:
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
            members.append(line[:-1])
        fil.close()
        return members

    def getRooms( self ):
        return self.rooms