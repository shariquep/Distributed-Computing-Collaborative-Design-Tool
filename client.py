import socket
import json
import threading
from _thread import start_new_thread


# serverAddressPortConnect   = ("127.0.0.1", 20001)
# hostPort = 20003
bufferSize = 1024
localIP = "127.0.0.1"

class Node:

    def __init__(self):
        self.host = False
        self.connectPort = (localIP, 20001)
        self.baseHostPort = 30001
        self.datagram = {}
        print("Establishing Connection ...")
        self.connectSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.datagram["name"] = input("Input Name: ")
        self.datagram["request_type"] = input("create session or join: ")
        
        if self.datagram["request_type"] == "join":
            self.datagram["key"] = input("Input key: ")

        self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectPort)
        self.datagram = json.loads(self.connectSocket.recvfrom(bufferSize)[0])

        if self.datagram["request_type"] == "create":
            self.createSession()
        elif self.datagram["request_type"] == "join":
            self.joinSession()
    

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

            send = threading.Thread(target=self.sendMessage,  daemon=True)
            read = threading.Thread(target=self.readMessage,  daemon=True)

            send.start()
            read.start()

            send.join()

    
    def sendMessage(self):
        if self.host:
            message = input()
            self.datagram["message"] = message
            for address in self.session["clients"]:
                self.hostSocket.sendto(str.encode(json.dumps(self.datagram)), address)

        else:
            while(True):
                message = input()
                self.datagram["message"] = message
                self.connectSocket.sendto(str.encode(json.dumps(self.datagram)), self.connectedHostAdd)
        pass

    def readMessage(self):
        if self.host:
            while(True):
                raw, clientAdd = self.hostSocket.recvfrom(bufferSize)
                self.response = json.loads(raw)
                print(self.response["message"])
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
                    print(self.response["message"])
                    
        pass



# hostport = 0    

# def getResponse(socket):
#     while(True):
#         response = json.loads(socket.recvfrom(bufferSize)[0])
#         print(response["message"])

# def sendRequest(socket,response,host):
#     while(True):
#         message = input()
#         response["message"] = message
#         socket.sendto(str.encode(json.dumps(response)), host)
        

# def joinSession(response,socket):
#     if response["key"] == None:
#         print("Invalid key")
#     else:
#         hostAdd = (response["host"][0],response["host"][1])
#         socket.sendto(str.encode(json.dumps(response)), hostAdd)

#         sendMessage = threading.Thread(target=sendRequest, args=(socket,response,hostAdd,), daemon=True)
#         recieveMessage = threading.Thread(target=getResponse, args=(socket,), daemon=True)

#         sendMessage.start()
#         recieveMessage.start()

#         sendMessage.join()

# def hostRecieve(socket):
#     while(True):
#         response = json.loads(socket.recvfrom(bufferSize)[0])
#         print(response["message"])

# def hostSend():
#     pass


    
if __name__ == "__main__":
    node = Node()