import random
import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 7788 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
players = dict([])
pets = dict([])

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

def clientthread(conn):
    id=random.randint(0,100000)
    global players
    global pets

    conn.sendall(str(id))

    while True:
        #Receiving from client
        data = conn.recv(1024)
        if data:
            action, value = data.split("_")
            if action == "up":
                print("up")
                for k, v in players.iteritems():
                    conn.sendall("pl_" + str(k) + "_" + str(v))
                for k, v in pets.iteritems():
                    conn.sendall("pt_" + str(k) + "_" + str(v))
                #update the dude
            elif action == "pl":
                print("pl")
                x,y,dx,dy = value.split(":")
                assert(x and y and dx and dy)
                players[id] = value
                #update his pos
            elif action == "pt":
                print("pt")
                x,y,dx,dy = value.split(":")
                assert(x and y and dx and dy)
                pets[id] = value
                #update his pet
        else:
            break

    del players[id]
    conn.close()

while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, ))

s.close()
