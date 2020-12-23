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


delim = ';'

BUFSIZ = 4096

myPort = 25000
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.bind(("", myPort))
# sock.bind((socket.gethostbyname(socket.gethostname()), myPort))

myUID = None # Replace with the proper user unique ID

socketManager = selectors.DefaultSelector()
socketManager.register( sock, selectors.EVENT_READ, None )

# chatroom_UIDs = []
active_chatroom = None

serverIP = str(input('Enter the server IP address: '))
serverPort = 25000
server = (serverIP, serverPort)
sendPrefix = str(myUID) + ';' # + str(priv_ip) + ';' + str(myPort)


# ! TODO IF NOT PUBLICLY HOSTING
# # virtually connect to server
# # print("punching")
# sock.sendto(b'', server)
# sock.sendto(b'', server)
# sock.sendto(b'', server)
# sock.sendto(b'', server)
# sock.sendto(b'', server)
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

def tokenize( obj ):
    obj = obj.decode()
    tokens = [elem.strip() for elem in obj.split(delim)]
    return tokens

def deTokenize( tokens ):
    for i in range(len(tokens)): tokens[i] = tokens[i].strip()
    msg = delim.join(tokens)
    return msg.encode('utf-8')

def connect():
    global sendPrefix
    sendPrefix = str(myUID) + delim
    msg = sendPrefix + 'online'
    while True:
        try:
            sock.connect(server)
            print('CONNECTED')
            break
        except:
            pass

def stop():
    msg = sendPrefix + 'ofline'
    msg = msg.encode('utf-8')
    sock.sendall(msg)
    sock.close(server)

def send(chatroom, chatroom_UIDs, timestamp = None, msg = '' ):

    tmp = msg

    if not timestamp:
        timestamp = time.time()
    for contact in chatroom_UIDs:
        print(msg)
        msg = sendPrefix + "addmsg;" + str(contact) + ';' + str(chatroom) + ';' + str(timestamp) + ';' + tmp
        msg = msg.encode("UTF-8") # encode the string
        sock.sendall(msg)  # sends message

def recv( ):
    queryList = []
    events = socketManager.select( timeout = 0.01 )
    for (key, mask) in events:
        data, addr = sock.recvfrom(BUFSIZ)

        if data:
            print('address: ', addr, '\ndata: ', data, sep = '')

            tokens = tokenize( data )

            if(tokens[0] == 'create'):
                people = []
                for person in tokens[2:]: people.append(person)
                tokens = tokens[:2]
                tokens.append(people)

            queryList.append(tokens)

            # create;room_name;[people in room by UID]
            # delete;room_name
            # addper;room_name;person
            # remper;room_name;person
            # addmsg;room_name;timestamp;sender;message

    return queryList

def createforothers( chatroom, uids, target = None ):
    if target is None:
        for uid in uids:
            msg = sendPrefix + 'create' + delim + str(uid) + delim + str(chatroom) + delim + delim.join(uids)
            msg = msg.encode('utf-8')
            sock.sendall(msg)
    else:
        msg = sendPrefix + 'create' + delim + str(target) + delim + str(chatroom) + delim + delim.join(uids)
        msg = msg.encode('utf-8')
        sock.sendall(msg)

def remove( chatroom, uids ):
    for uid in uids:
        msg = sendPrefix + 'remper' + delim + str(uid) + delim + str(chatroom) + delim + str(myUID)
        msg = msg.encode('utf-8')
        sock.sendall(msg)

def add( chatroom, uids , targetUID):
    for uid in uids:
        msg = sendPrefix + 'addper' + delim + str(uid) + delim + str(chatroom) + delim + str(targetUID)
        msg = msg.encode('utf-8')
        sock.sendall(msg)

    uids.append(targetUID)
    createforothers(chatroom, uids, targetUID)