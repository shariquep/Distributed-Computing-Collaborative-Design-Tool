from tkinter import *
from tkinter import ttk, colorchooser
import multiprocessing
import json
from _thread import start_new_thread



class main:
    def __init__(self,master,pipe):
        self.params = {} 
        self.guiPipe = pipe
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        start_new_thread(self.acceptCommand, ('dummy',))


    def paint(self,e):
        

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y
        
        if "x" in self.params:
            self.params["x"].append(self.old_x)
        else:        
            self.params["x"] = [self.old_x]
        
        if "y" in self.params:
            self.params["y"].append(self.old_y)
        else:        
            self.params["y"] = [self.old_y]
            


    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None
        self.params["width"] = self.penwidth
        self.params["fill"] = self.color_fg
        self.params["type"] = "pencil-Line"
        self.guiPipe.send(json.dumps(self.params))
        self.params = {}      

    def acceptCommand(self,dummy):
        
        while True:
            raw = self.guiPipe.recv()
            params = json.loads(raw)
            if params["type"] == "pencil-Line":
                if "x" in params and "y" in params:
                    x = params["x"]
                    y = params["y"]
                    width = params["width"]
                    col = params["fill"]
                    for i in range(1,len(x)):
                        self.c.create_line(x[i-1],y[i-1],x[i],y[i],width=width,fill=col,capstyle=ROUND,smooth=True)

            elif params["type"] == "clear":
                self.c.delete(ALL)

            elif params["type"] == "changeBG":    
                self.c['bg'] = params["bg"]

            params = {}

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e
           

    def clear(self):
        self.c.delete(ALL)
        self.params["type"] = "clear"
        self.guiPipe.send(json.dumps(self.params))
        self.params = {}

    def change_fg(self):  #changing the pen color
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #changing the background color canvas
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg
        self.params["type"] = "changeBG"
        self.params["bg"] = self.color_bg
        self.guiPipe.send(json.dumps(self.params))
        self.params = {}

    def save_canvas(self):  #changing the background color canvas
        print("Saved")

    def drawWidgets(self):

        self.master.config(bg="skyblue") # specify background color
        # Create top and bottom frames
        top_frame = Frame(self.master, width=500, height=200, bg='white')
        top_frame.grid(row=0, column=0, padx=10, pady=5,ipady=5,ipadx=5)
        bottom_frame = Frame(self.master, width=550, height=600, bg='grey')
        bottom_frame.grid(row=1, column=0, padx=10, pady=5)
            
        # Create frames and labels in left_frame 
        Label(top_frame, text="Session Code: ").grid(row=0, column=0,pady=5)

        fg_btn =Button(top_frame, text="Pen Color",command=self.change_fg)
        fg_btn.grid(row=1, column=0)

        bg_btn =Button(top_frame, text="BG Color",command=self.change_bg)
        bg_btn.grid(row=1, column=1)

        circle_btn =Button(top_frame, text="Circle")
        circle_btn.grid(row=1, column=2)

        rect_btn =Button(top_frame, text="Rect")
        rect_btn.grid(row=1, column=3)

        
        Label(top_frame, text='Pen Width:').grid(row=1,column=4,padx= 5)
        self.slider = ttk.Scale(top_frame,from_= 5, to = 100,command=self.changeW,orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=1,column=5,ipadx=10,padx=5)

        
        save_btn =Button(top_frame, text="Save",command= self.save_canvas)
        save_btn.grid(row=1, column=6,padx=15)
            
            
        # Display canvas in right_frame
        self.c = Canvas(bottom_frame,width=500,height=500,bg=self.color_bg,)
        self.c.grid(row=0,column=0, padx=5, pady=5)


