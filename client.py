import socket
import json
import threading
from _thread import start_new_thread
import interface
import multiprocessing


# serverAddressPortConnect   = ("127.0.0.1", 20001)
# hostPort = 20003
bufferSize = 1024*1024
localIP = "127.0.0.1"

class Node:

    def __init__(self):
        self.guiPipe, self.nodePipe = multiprocessing.Pipe()
        self.permissionPipe, self.p2nPipe = multiprocessing.Pipe()
        self.host = False
        self.connectPort = (localIP, 20001)
        self.baseHostPort = 30001
        self.datagram = {}
        self.history = []
        print("Establishing Connection ...")
        self.connectSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.startWindow()

        self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectPort)
        self.datagram = json.loads(self.connectSocket.recvfrom(bufferSize)[0])


        if self.datagram["request_type"] == "create":
            self.createSession()
        elif self.datagram["request_type"] == "join":
            self.joinSession()
    
    def startWindow(self):
        name,request_type,key=interface.display()
        self.datagram["name"] = name
        self.datagram["request_type"] = request_type
        if(request_type == "join"):
            self.datagram["key"] = key



    def acceptNewClient(self,raw,clientAddress):
        self.datagram = json.loads(raw)
        self.datagram["newPort"] = self.hostPort
        print(self.datagram["name"] + "joined")
        self.p2nPipe.send((self.datagram["name"],self.session["clients"][-1]))
        self.datagram["PortUpdate"] = True
        self.datagram["history"] = self.history
        self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), clientAddress)
        self.datagram.pop("history")
        self.datagram["PortUpdate"] = False
        send = threading.Thread(target=self.sendMessage, daemon=True)
        read = threading.Thread(target=self.readMessage, daemon=True)

        send.start()
        read.start()

        send.join()
        read.join()

    def createSession(self):
        self.host = True 
        print("Session created with key: " + self.datagram["key"])
        self.session = self.datagram["session"]
        self.hostPort = self.baseHostPort + self.datagram["port_offset"]
        self.hostSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.hostSocket.bind((localIP, self.hostPort))
        
        start_new_thread(interface.startPaint, (self.guiPipe,self.datagram["key"],True,))
        start_new_thread(interface.startPermission, (self.permissionPipe,))
        readPermission = threading.Thread(target=self.readPermission, daemon=True)
        readPermission.start()

        while(True):
            raw,clientAddress = self.connectSocket.recvfrom(bufferSize)
            self.session["clients"].append(clientAddress)

            start_new_thread(self.acceptNewClient, (raw,clientAddress,))

    def joinSession(self):
        if self.datagram["host"] == None:
            print("Invalid key")
            exit()
        else:
            self.connectedHostAdd = (self.datagram["host"][0],self.datagram["host"][1])
            self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectedHostAdd)
            
            start_new_thread(interface.startPaint, (self.guiPipe,self.datagram["key"],False))
            
            send = threading.Thread(target=self.sendMessage,  daemon=True)
            read = threading.Thread(target=self.readMessage,  daemon=True)
            

            send.start()
            read.start()

            send.join()

    
    def sendMessage(self):
        while True:
            if self.host:
                message = self.nodePipe.recv()
                self.history.append(json.loads(message))
                
                if "clearCanvas" in message:
                    self.history = []
                
                self.datagram["message"] = message
                for address in self.session["clients"]:
                    self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), address)

            else:
                message = self.nodePipe.recv()
                self.datagram["message"] = message
                self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectedHostAdd)

    def readMessage(self):
        while True:
            if self.host:
                raw, clientAdd = self.hostSocket.recvfrom(bufferSize)
                self.response = json.loads(raw)
                print(json.loads(self.response["message"]))
                self.history.append(json.loads(self.response["message"]))
                self.nodePipe.send(self.response["message"])
                self.datagram["message"] = self.response["message"]
                for address in self.session["clients"]:
                    if address != clientAdd:
                        self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), address)

            else:
                self.response = json.loads(self.connectSocket.recvfrom(bufferSize)[0])
                if self.response["PortUpdate"]:
                    self.connectedHostAdd = (self.connectedHostAdd[0], self.response["newPort"])
                    self.nodePipe.send(json.dumps(self.response["history"]))
                else:
                    self.nodePipe.send(self.response["message"])

    def readPermission(self):
        while True:
            self.datagram["message"],add = self.p2nPipe.recv()
            self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), add)



    
if __name__ == "__main__":
    node = Node()