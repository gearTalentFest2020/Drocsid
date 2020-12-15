import os, sys

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
        # The UID generation code comes here
        return "a"

    def __getitem__( self, key ):
        return self.contacts[key]