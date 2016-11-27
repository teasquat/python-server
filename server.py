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
    player_id=random.randint(0,100000)
    global players
    global pets

    pet = 1
    beard = 1
    br = 1
    bg = 1
    bb = 1
    tshirt = 1
    tr = 1
    tg = 1
    tb = 1

    conn.sendall(str(player_id))

    while True:
        #Receiving from client
        data = conn.recv(1024)
        exit = False

        for part in iter(data.splitlines()):
            if part == "close": exit = True; break
            if (part.count("_") != 1): break
            action, value = part.split("_")
            if action == "up":
                for k, v in players.iteritems():
                    conn.sendall("pl_" + str(k) + "_" + str(v) + "\n")
                for k, v in pets.iteritems():
                    conn.sendall("pt_" + str(k) + "_" + str(v) + "\n")
                conn.sendall("done\n")
                #update the dude
            elif action == "pl":
                if (part.count(":") != 3): break
                x,y,dx,dy = value.split(":")
                if (not (x and y and dx and dy)): break
                players[player_id] = value
                #update his pos
            elif action == "pt":
                if (part.count(":") != 3): break
                x,y,dx,dy = value.split(":")
                if (not (x and y and dx and dy)): break
                pets[player_id] = value
                #update his pet
            elif action == "id":
                player_id = value
            elif action == "sp":
                if (part.count(":") != 8): break
                pet, beard, br, bg, bb, tshirt, tr, tg, tb = value.split(":")

        if exit: conn.sendall("kys"); break

    del players[player_id]
    del pets[player_id]
    conn.close()

while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, ))

s.close()
