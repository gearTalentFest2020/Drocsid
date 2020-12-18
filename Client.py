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
    tmp = msg
    for contact in chatroom_UIDs:
        print(msg)
        msg = sendPrefix + "send;" + str(contact) + ';' + str(chatroom) + ';' + str(timestamp) + ';' + tmp
        msg = msg.encode("UTF-8") # encode the string
        sock.sendto(msg, server)  # sends message

def recv( ):
    queryList = []
    events = socketManager.select( timeout = 0.01 )
    for (key, mask) in events:
        data, addr = sock.recvfrom(BUFSIZ)
        data = data.decode()

        if data:
            print('address:', addr)
            print(data)

            tokens = data.split(';')
            query = []

            if(tokens[0] == 'recv'):
                name = tokens[1]
                sender = tokens[2]
                timestamp = tokens[3]
                msg = ";".join(tokens[4:])
                query += ['addmsg', name, timestamp, sender, msg]

            elif(tokens[0] == 'create'):
                name = tokens[1]
                members = tokens[2:]
                query += ['create', name, members]

            elif(tokens[0] == 'remove'):
                name = tokens[1]
                sender = tokens[2]
                query += ['remove', name, sender]

            elif(tokens[0] == 'addper'):
                name = tokens[1]
                toAdd = tokens[2]
                query += ['addper', tokens[1], tokens[2]]

            queryList.append(query)
    return queryList

def createforothers( chatroom, uids , target = None ):
    if target is None:
        for uid in uids:
            msg = sendPrefix + 'create;' + str(uid) + ';' + str(chatroom) + ';' + ';'.join(uids)
            msg = msg.encode('utf-8')
            sock.sendto(msg, server)
    else:
        msg = sendPrefix + 'create;' + str(target) + ';' + str(chatroom) + ';' + ';'.join(uids)
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
    uids.append(targetUID)
    uids.remove(myUID)
    createforothers(chatroom, uids, targetUID)

def stop():
    msg = sendPrefix + 'ofline'
    msg = msg.encode('utf-8')
    sock.sendto(msg, server)

