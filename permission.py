from tkinter import *
from functools import partial

def printRights(user):
    if user["access"].get() == 1:
        print("user {} has read-write access".format(user["name"]))
    else:
        print("user {} has read only access".format(user["name"]))

def addUser():
    c = Checkbutton(window, text=users[-1]["name"], 
                    variable=users[-1]["access"],
                    onvalue=1, offvalue=0,
                    command=partial(printRights, users[-1]))
    c.pack()
    # this line is just to check the dynamic func, remove it 
    users.append({"name": "hal", "access": IntVar()})

window = Tk()
window_label = Label(text="Participants:",
                     width=20, height=3)
window_label.pack()

# usernames to be displayed should be dynamically appended to
# this list, and whenever a new user is appended,
# call the addUser() function to update the checkbox screen
users = [{"name": "sha", "access": IntVar()}]

######## remove this button, only added to see if the function works
b = Button(window, text="Add a checkbox", command=addUser)
b.pack()
#########

window.mainloop()