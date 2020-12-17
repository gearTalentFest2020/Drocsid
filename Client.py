# Client tells server he is online
# UID;online

# Client tells server he is offline
# UID;ofline

# Client tells server to create a chatroom
# UID;create;targetUID;chatroomname;[; seperated UIDs of members]

# targetUID goes thru each of the UIDs of people present in the chatroon
# This will work for initial creation and addition, by proper if statements
# and changing the targetUID

# Client tells server to remove themselves from a chatroom
# UID;remove;targetUID;chatroomname

# Client send a message on a particular chatroom
# UID;send;targetUID;chatroomname;msg


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

# chatroom_UIDs = []
active_chatroom = None

serverIP = str(input('Enter the server IP address: '))
serverPort = 16384
server = (serverIP, serverPort)
sendPrefix = str(myUID) + ';' # + str(priv_ip) + ';' + str(myPort)


# ! TODO IF NOT PUBLICLY HOSTING
# # virtually connect to server
# # print("punching")
sock.sendto(b'', server)
sock.sendto(b'', server)
data, addr = sock.recvfrom(BUFSIZ)
print(addr)
sock.sendto(b'', server)
sock.sendto(b'', server)
sock.sendto(b'', server)
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

def connect():
    global sendPrefix
    sendPrefix = str(myUID) + ';'
    msg = sendPrefix + 'online'
    msg = msg.encode('utf-8')
    sock.sendto(msg, server)

def send(chatroom, chatroom_UIDs, timestamp=None, msg = '' ):
    if not timestamp: timestamp = time.time()
    for contact in chatroom_UIDs:
        msg = sendPrefix + "send;" + str(contact) + ';' + str(chatroom) + ';' + str(timestamp) + ';' + msg
        msg = msg.encode("UTF-8") # encode the string
        sock.sendto(msg, server)  # sends message

def recv( ):
    queryList = []
    events = socketManager.select( timeout = 0.01 )
    for (key, mask) in events:
        data, addr = sock.recvfrom(BUFSIZ)
        data = data.decode()
        print('address:', addr)
        print(data)
        if data:

            tokens = data.split(';')
            query = []

            if(tokens[0] == 'recv'):
                name = tokens[1]
                sender = tokens[2]
                msg = tokens[3].split(';')[1]
                timestamp = tokens[3].split(';')[0]
                query.append('addmsg')
                query.append(name)
                query.append(timestamp)
                query.append(sender)
                query.append(msg)

            elif(tokens[0] == 'create'):
                name = tokens[1]
                members = tokens[2:].split(';')
                query.append('create')
                query.append(name)
                query.append(members)

            elif(tokens[0] == 'remove'):
                name = tokens[1]
                sender = tokens[2]
                query.append('remove')
                query.append(name)
                query.append(sender)

            elif(tokens[0] == 'addper'):
                query.append('addper')
                query.append(tokens[1])
                query.append(tokens[2])

            queryList.append(query)
    return queryList

def createforothers( chatroom, uids ):
    for uid in uids:
        msg = sendPrefix + 'create;' + str(uid) + ';' + str(chatroom) + ';' + ';'.join(uids)
        msg = msg.encode('utf-8')
        sock.sendto(msg, server)

def remove( chatroom, uids ):
    for uid in uids:
        msg = sendPrefix + 'remove;' + str(uid) + ';' + str(chatroom)
        msg = msg.encode('utf-8')
        sock.sendto(msg, server)

def add( chatroom, uids , targetUID):
    for uid in uids:
        msg = sendPrefix + 'addper;' + str(uid) + ';' + str(chatroom) + ';' + str(targetUID)
        msg = msg.encode('utf-8')
        sock.sendto(msg, server)

def stop():
    msg = sendPrefix + 'ofline'
    msg = msg.encode('utf-8')
    sock.sendto(msg, server)

