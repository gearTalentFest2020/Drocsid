import os, sys, json
import socket, time
from baseChange import *

import hashlib
import Client

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

        return self.UID

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
        return self.contacts.get(key, None)

class memberManager:

    def __init__( self, filePath ):
        self.members = []
        self.filePath = filePath

    def loadAll( self ):
        f = open(self.filePath, 'r')
        lines = f.readlines()
        for line in lines:
            UID = line[:-1]
            self.members.append(UID)
        f.close()

    def update( self ):
        f = open(filePath, 'w')
        for UID in self.members:
            f.write(UID + '\n')
        f.close()

    def saveAll( self ):
        self.update()

    def __getitem__( self, key ):
        return self.members[key]

    def __setitem__( self, key, value ):
        self.members[key] = value
        self.update()

class chatroomManager:

    def __init__( self ):
        # Something comes here
        pass

    def addMemberTo( self, chatroom, UID ):
        fil = open('chatroom__'+chatroom+'/People.txt', 'r')
        members = [UID]
        lines = fil.readlines()
        for line in lines:
            line = line[:-1]
            members.append(line)
        fil.close()
        fil = open('chatroom__'+chatroom+'/People.txt', 'r')
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
        fil = open('chatroom__'+chatroom+'/People.txt', 'r')
        for member in members:
            fil.write(member + '\n')
        fil.close()

    def addMsgTo( self, chatroom, message ):
        chatroom = 'chatroom__' + chatroom
        # DB code comes here

    def deleteRoom( self, chatroom ):
        chatroom = 'chatroom__' + chatroom
        try:
            for fil in os.listdir(chatroom): os.remove(chatroom + '/' + fil)
            os.rmdir(chatroom)
        except:
            pass