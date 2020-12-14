import os, sys

class contactsManager:

    def __init__( self ):
        self.contacts = {}
        open('Contacts.txt', 'w') if(not os.path.exists('Contacts.txt')) else None

    def loadAll( self ):
        contacts_file = open('Contacts.txt', 'r')

        for line in contacts_file.readlines():
            tokens = line.split(';')
            tokens[2] = tokens[2][:-1]
            assert len(tokens)==3, "Corrupted Contacts File"
            self.contacts.setdefault(tokens[0], [tokens[1], tokens[2]])
        contacts_file.close()

    def saveAll( self ):
        contacts_file = open('Contacts.txt', 'w')
        for ID in self.contacts: contacts_file.write(ID + ";" + self.contacts[ID][0] + ";" + self.contacts[ID][1] + '\n')

    def addContact( self, ID, name, ip ):
        self.contacts.setdefault(ID.strip(), [name.strip(), ip.strip()])

    def remContact( self, ID ):
        self.contacts.pop( ID.strip() )

    def altContact( self, ID, name, ip ):
        self.contacts[ID.strip()][0] = name.strip()
        self.contacts[ID.strip()][1] = ip.strip()

    def __getitem__( self, key ):
        return self.contacts[key]