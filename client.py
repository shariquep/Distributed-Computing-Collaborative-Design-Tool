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
        self.host = False
        self.connectPort = (localIP, 20001)
        self.baseHostPort = 30001
        self.datagram = {}
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
        self.datagram["PortUpdate"] = True
        self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), clientAddress)
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
        
        start_new_thread(interface.startPaint, (self.guiPipe,))

        while(True):
            raw,clientAddress = self.connectSocket.recvfrom(bufferSize)
            self.session["clients"].append(clientAddress)

            start_new_thread(self.acceptNewClient, (raw,clientAddress,))

    def joinSession(self):
        if self.datagram["key"] == None:
            print("Invalid key")
        else:
            self.connectedHostAdd = (self.datagram["host"][0],self.datagram["host"][1])
            self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectedHostAdd)
            
            start_new_thread(interface.startPaint, (self.guiPipe,))
            
            send = threading.Thread(target=self.sendMessage,  daemon=True)
            read = threading.Thread(target=self.readMessage,  daemon=True)
            

            send.start()
            read.start()

            send.join()

    
    def sendMessage(self):
        if self.host:
            while True:
                message = self.nodePipe.recv()
                self.datagram["message"] = message
                for address in self.session["clients"]:
                    self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), address)

        else:
            while(True):
                message = self.nodePipe.recv()
                self.datagram["message"] = message
                self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectedHostAdd)
        pass

    def readMessage(self):
        if self.host:
            while(True):
                raw, clientAdd = self.hostSocket.recvfrom(bufferSize)
                self.response = json.loads(raw)
                self.nodePipe.send(self.response["message"])
                self.datagram["message"] = self.response["message"]
                for address in self.session["clients"]:
                    if address != clientAdd:
                        self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), address)

        else:
            while(True):
                self.response = json.loads(self.connectSocket.recvfrom(bufferSize)[0])
                if self.response["PortUpdate"]:
                    self.connectedHostAdd = (self.connectedHostAdd[0], self.response["newPort"])
                else:
                    self.nodePipe.send(self.response["message"])
                    
        pass

    
if __name__ == "__main__":
    node = Node()