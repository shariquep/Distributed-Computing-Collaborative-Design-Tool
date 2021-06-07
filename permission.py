from tkinter import *
from functools import partial
from _thread import start_new_thread
import json

class permission:

    def __init__(self,master,pipe):
        self.master = master
        self.pipe = pipe
        self.users = []
        Label(self.master, text="Edit Permission for Users:",width=20, height=3).pack()
        start_new_thread(self.acceptClient, ('dummy',))
        

    def changeRights(self,user):
        data = {}
        data["name"] = user["name"]
        data["address"] = user["address"]
        
        if user["access"].get() == 1:
            data["access"] = 1
        else:
            data["access"] = 0
        
        data["type"] = "changePermission"
        print("permission side:")
        print(self.users)
        self.pipe.send((json.dumps(data),data["address"]))


    def addUser(self):
        Checkbutton(self.master, text="  " + self.users[-1]["name"], 
                        variable=self.users[-1]["access"],
                        onvalue=1, offvalue=0,
                        command= partial(self.changeRights,self.users[-1])).pack()

    def acceptClient(self,dummy):
        while True:
            name,address = self.pipe.recv()
            user = {}
            user["name"] = name
            user["address"] = address
            user["access"] = IntVar()
            self.users.append(user)
            self.addUser()
