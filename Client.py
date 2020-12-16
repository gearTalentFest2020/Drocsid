import socket, sqlite3
import pickle, bz2
import selectors, multiprocessing
import sys, os

BUFSIZ = 4096

myPort = 16384
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.bind(("", myPort))
# sock.bind((socket.gethostbyname(socket.gethostname()), myPort))

UID = None # Replace with the proper user unique ID

socketManager = selectors.DefaultSelector()
socketManager.register( sock, selectors.EVENT_READ, None )

chatroom_UIDs = []
active_chatroom = None

priv_ip = socket.gethostbyname(socket.gethostname())
serverIP = '35.233.187.196'
serverPort = 16384
server = (serverIP, serverPort)
sendPrefix = str(UID) + ';' # + str(priv_ip) + ';' + str(myPort)


# ! TODO IF NOT PUBLICLY HOSTING
# virtually connect to server
# print("punching")
sock.sendto(b'', server)
data, addr = sock.recvfrom(BUFSIZ)
# print(addr)
sock.sendto('1VsV3V;online'.encode('utf-8'), server)
sock.sendto('1VsV3V;online'.encode('utf-8'), server)
sock.sendto('1VsV3V;send;1VsV3V;chatroom;helloworld'.encode('utf-8'), server)
# print("punched")
sock.setblocking( False )

def genUID():
    pass

def send( msg = '' ):
    m = "hello world"
    for contact in chatroom_UIDs:
        msg = sendPrefix + "send;" + str(contact) + ';' + str(active_chatroom) + ';' + m
        msg = msg.encode("UTF-8") # encode the string
        sock.sendto(msg, server)  # sends message

def recv():
    events = socketManager.select( timeout = 0.01 )
    for (key, mask) in events:
        data, addr = sock.recvfrom(BUFSIZ)
        data = data.decode()
        print('address:', addr)
        if data:
            print(serverIP + ': ' + str(data))

def create():
    m = sendPrefix + 'create;'

def remove():
    m = sendPrefix + 'remove;'

def stop():
    m = sendPrefix + 'exit;'


target = 'chats'

def create( self , chatroom ):
    self.name  =  chatroom + '/' + target + '.db'
    self.conn  =  sqlite3.connect( self.name )
    c = self.conn.cursor()
    try:
        ## Create Table
        c.execute( '''CREATE TABLE chat(time INTEGER NOT NULL PRIMARY KEY, sender TEXT, msg TEXT)''' )
        self.conn.commit()

    except Exception as e:
        # print(e)
        pass

## Save method
def save( self, key, t , chatroom ):
    c = self.conn.cursor()
    try:
        ## Save string at new key location
        c.execute( '''INSERT INTO chat (time, sender, msg) VALUES (?,?,?)''', ( key, bz2.compress( t[0] ), bz2.compress( t[1] ) ) )
        self.conn.commit()

    except Exception as e:
        # print(e)
        ## Update string at existing key
        # c.execute( 'UPDATE terrain SET list =?, local =?  WHERE keys=?', ( bz2.compress( t[0] ), bz2.compress( t[1] ), key ) )
        # self.conn.commit()
        pass

## Load method
def get( self, key, chatroom ):
    c = self.conn.cursor()
    c.execute('''SELECT sender FROM chat WHERE time=?''', (key,))
    sender = c.fetchone()
    c.execute('''SELECT msg FROM chat WHERE time=?''', (key,))
    msg = c.fetchone()
    self.conn.commit()

    try:
        li = bz2.decompress( sender[0] )
        lo = bz2.decompress( msg[0] )
        return sender, msg
    except Exception as e:
        # print(e)
        return None