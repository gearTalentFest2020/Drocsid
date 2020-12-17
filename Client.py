import socket, sqlite3
import pickle, bz2, time
import selectors, multiprocessing
import sys, os

BUFSIZ = 4096

myPort = 16384
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.bind(("", myPort))
# sock.bind((socket.gethostbyname(socket.gethostname()), myPort))

myUID = None # Replace with the proper user unique ID

socketManager = selectors.DefaultSelector()
socketManager.register( sock, selectors.EVENT_READ, None )

chatroom_UIDs = []
active_chatroom = None

priv_ip = socket.gethostbyname(socket.gethostname())
serverIP = '104.196.65.135'
serverPort = 16384
server = (serverIP, serverPort)
sendPrefix = str(myUID) + ';' # + str(priv_ip) + ';' + str(myPort)


# ! TODO IF NOT PUBLICLY HOSTING
# # virtually connect to server
# # print("punching")
# sock.sendto(b'', server)
# data, addr = sock.recvfrom(BUFSIZ)
# print(addr)
# sock.sendto('1VsV3V;online'.encode('utf-8'), server)
# time.sleep(3)
# print('Sending 2nd time')
# sock.sendto('1VsV3V;online'.encode('utf-8'), server)
# time.sleep(1)
# sock.sendto('1VsV3V;create;1VsV3V;mytestchat;abc123;xyz456'.encode('utf-8'), server)
# time.sleep(1)
# sock.sendto('1VsV3V;send;1VsV3V;mytestchat;arandomthing1234'.encode('utf-8'), server)
# time.sleep(1)
# sock.sendto('1VsV3V;remove;abc123;mytestchat'.encode('utf-8'), server)
# time.sleep(1)
# # print("punched")
# sock.sendto('1VsV3V;ofline'.encode('utf-8'), server)
sock.setblocking( False )

def genUID():
    pass

def send( msg = '', timestamp=None ):
    if not timestamp: timestamp = time.time()
    save(active_chatroom, timestamp, myUID, msg)
    for contact in chatroom_UIDs:
        msg = sendPrefix + "send;" + str(contact) + ';' + str(active_chatroom) + ';' + msg
        msg = msg.encode("UTF-8") # encode the string
        sock.sendto(msg, server)  # sends message

def recv():
    events = socketManager.select( timeout = 0.01 )
    for (key, mask) in events:
        data, addr = sock.recvfrom(BUFSIZ)
        data = data.decode()
        print('address:', addr)
        print(data)
        if data:

            tokens = data.split(';')

            if(tokens[0] == 'recv'):
                name = "chatroom__" + tokens[1]
                sender = tokens[2]
                msg = tokens[3]
                save(name, str(time.time()), sender, msg)

            elif(tokens[0] == 'create'):
                name = tokens[1]
                members = tokens[2:]

                name = "chatroom__" + name

                try: os.mkdir( name )
                except: pass

                open(name + '/People.txt', 'w') if(not os.path.exists(name + '/People.txt')) else None
                f = open(name + '/People.txt', 'w')
                for member in members: f.write(member + '\n')

                create( name )

            elif(tokens[0] == 'remove'):
                name = tokens[1]
                sender = tokens[2]

                members = []

                f = open('chatroom__' + name + '/People.txt', 'r')
                lines = f.readlines()
                for line in lines:
                    line = line[:-1]
                    if(line != sender): members.append(line)

                f.close()
                f = open('chatroom__' + name + '/People.txt', 'r')
                for member in members:
                    f.write(member + '\n')
                f.close()
                print(members)

def createforothers(chatroom, uids):
    m = sendPrefix + 'create;' + str(chatroom) + ';' + ';'.join(uids)

def remove():
    m = sendPrefix + 'remove;'

def stop():
    m = sendPrefix + 'ofline'


target = 'chats'

def create( chatroom ):
    name  =  chatroom + '/' + target + '.db'
    conn  =  sqlite3.connect( name )
    c = conn.cursor()
    try:
        ## Create Table
        c.execute( '''CREATE TABLE chat(time REAL NOT NULL PRIMARY KEY, sender TEXT, msg TEXT)''' )
        conn.commit()

    except Exception as e:
        # print(e)
        pass
    conn.close()

## Save method
def save( chatroom, key, sender , msg):
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

## Load method
def get( key, chatroom, n = 50 ):
    name  =  chatroom + '/' + target + '.db'
    conn  =  sqlite3.connect( name )
    c = conn.cursor()
    c.execute('''SELECT time, sender, msg FROM chat''')
    l = c.fetchall()
    conn.commit()
    conn.close()
    return l[-1:-n-1:-1][::-1]
