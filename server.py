import socket
import json
import string    
import random
import threading
from _thread import start_new_thread

newClientport   = 20001
pingHostPort = 20002
sessions = {}
clientList = {}
bufferSize = 1024
localIP = "127.0.0.1"
keys = []

def initializeConn():
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, newClientport))
    UDPHostSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPHostSocket.bind((localIP, pingHostPort))
    print("Connection established! ready for clients . . .")
    return UDPServerSocket,UDPHostSocket

def pingHost():
    
    while(True):
        continue

def acceptNewCleint(UDPsocket,raw,clientAddress):

    request = json.loads(raw)
    print("request from " + request["name"])
    if request["request_type"] == "create":
        key = generatekey(10)
        keys.append(key)
        request["port_offset"] = len(keys)
        print("key generated "+key)
        session = {}
        session["host"] = clientAddress
        session["clients"] = []
        sessions[key] = session
        request["key"] = key
        request["session"] = session
        UDPsocket.sendto(str.encode(json.dumps(request)),clientAddress)
        pingHost()

    elif request["request_type"] == "join":
        key = request["key"]
        if key in sessions.keys():
            request["host"] = sessions[key]["host"]
            sessions[key]["clients"].append(clientAddress)
        else:
            request["host"] = None

        UDPsocket.sendto(str.encode(json.dumps(request)),clientAddress)


    
    
def generatekey(length):
    
    while True:
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))
        if key not in sessions.keys():
            break

    return key

if __name__ == "__main__":
    incomingSocket,hostSocket = initializeConn() 
    while(True):
        raw,clientAddress = incomingSocket.recvfrom(bufferSize)
        start_new_thread(acceptNewCleint, (hostSocket,raw,clientAddress,))