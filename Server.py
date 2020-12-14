import socket, sqlite3
import pickle, zlib
import selectors
import sys, os

port = 16384
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", port))

# Keys are phone numbers, values are [pubIp, pubPort, privIp, privPort]
ip_table = {}
createRequests = []

while True:
    # Broadcast garbage msg to everyone on the port
    sock.sendto(b'', ('<broadcast>', port))
    # Accept a msg from some client user
    data, addr = sock.recvfrom(1024)
    print('Connected to:', addr)
    # data_format = 'uniqeid;privIP;privPort;con/bye/...'

    tokens = data.split(';')
    # tokens[0] contains senders phone number (ALWAYS)
    # tokens[1] contains the type of request (ALWAYS)

    # tokens[2] contains
    #   the private ip (in case of ip sync)
    #   the recivers phone number (in case of ip request
    #   the recievers phone number (in case of creation of chatroom)
    #   the recievers phone number (in case of deletion of chatroom)

    # tokens[3] contains
    #   the private port (in case of ip sync)
    #   the name of the chatroom (in case of creation of chatroom)
    #   the name of the chatroom (in case of deletion of chatroom)

    # '<number1>;con/bye/create/delete;privip/number2;'

    # When you come online and go offline
    if(tokens[0] == 'con'):
        ip_table[tokens[1]] = list(addr)
    elif(tokens[0] == 'bye'):
        ip_table.pop(tokens[1])
    elif(tokens[0] == 'req'):
        toSend = ip_table.get(tokens[1], None)
        sock.sendto(toSend.encode("UTF8"), addr)
    elif(tokens[0] == 'create'):
        createRequests.append([])
    elif(tokens[0] == 'remove'):
        pass



# The server is always running
# The server must have a DB which stores all msgs sent to it

# Types of msgs-
# 1. Request to create a chatroom (contains sender, reciever and name) (This is the same even for adding people)
# 2. Request to remove a person from a chatroom (contains sender, reciever(s) and name)
# 3. Sending IP of self
# 4. Removing IP of self
# 5. Requesting IP of some phone number

# 1.
# This msg is kept until the target comes online after which it is sent and deleted
# 2.
# This msg is kept until the target comes online after which it is sent and deleted
# 3.
# This is sent to the server upon coming online
# 4.
# This is sent to the server before going offline
# 5.
# This is sent to the server after which the server responds
