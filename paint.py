from tkinter import *
from tkinter import ttk, colorchooser,font
import multiprocessing
import json
from _thread import start_new_thread
from helper import *


class main:
    def __init__(self,master,pipe,key):
        self.params = {} 
        self.helperFunc = {"pencilLine":pencilLine, "clearCanvas": clearCanvas, "changeBG": changeBG,
                            "drawRectangle":drawRectangle, "drawCircle": drawCircle, "straightLine":straightLine}
        self.key = key
        self.recordXY = True
        self.guiPipe = pipe
        self.master = master
        self.drawType = "Pen"
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.shape_color= 'None'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        start_new_thread(self.acceptCommand, ('dummy',))


    def paint(self,e):
        
        if self.drawType == "Pen":
            self.old_x, self.old_y, self.params = drawPencil(self.old_x, self.old_y,e,self.penwidth,
                                                            self.color_fg,self.params,self.c)
        elif self.recordXY:
            self.recordXY = False
            self.old_x = e.x
            self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas
        if self.drawType != "Pen":
            self.recordXY = True
            self.params["x1"] = self.old_x
            self.params["y1"] = self.old_y
            self.params["x2"] = e.x
            self.params["y2"] = e.y

            if self.drawType == "Rect":
                self.c.create_rectangle(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,outline=self.color_fg)
                self.params["type"] = "drawRectangle"

            elif self.drawType == "Circle":
                self.c.create_oval(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,outline=self.color_fg)
                self.params["type"] = "drawCircle"

            elif self.drawType == "Line":    
                self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
                self.params["type"] = "straightLine"
                
        else:
            self.params["type"] = "pencilLine"

        self.params["width"] = self.penwidth
        self.params["fill"] = self.color_fg
        self.guiPipe.send(json.dumps(self.params))
        self.params = {}      
        self.old_x = None
        self.old_y = None

    def restoreHistory(self,commands):
        for params in commands:
            self.helperFunc[params["type"]](self.c,params)
    
    def acceptCommand(self,dummy):
        
        while True:
            raw = self.guiPipe.recv()
            params = json.loads(raw)

            if type(params) is list:
                self.restoreHistory(params)

            else:
                self.helperFunc[params["type"]](self.c,params)
           
            params = {}

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e
           

    def clear(self):
        self.c.delete(ALL)
        self.params["type"] = "clearCanvas"
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

    def set_drawType(self,type):
        print("Type",type)
        self.drawType=type

    def save_canvas(self):  #changing the background color canvas
        print("Saved")

    def shapeFill(self,btn):
        if(btn['relief']=='raised'): 
            #SET shape_fill color
            self.shape_color = colorchooser.askcolor(title="Shape Fill Color")[1]
            btn.configure(relief = 'sunken',bg = self.shape_color,fg = self.shape_color)
            print(self.shape_color)
        else:
            self.shape_color='None'
            btn.configure(relief = 'raised',bg = 'light grey',fg='black',text='Fill')


    def drawWidgets(self):

        self.master.config(bg="skyblue") # specify background color
        # Create top and bottom frames
        top_frame = Frame(self.master, width=500, height=200, bg='white')
        top_frame.grid(row=0, column=0, padx=10, pady=5)
        bottom_frame = Frame(self.master, width=550, height=600, bg='grey')
        bottom_frame.grid(row=1, column=0, padx=10, pady=5)
            
        # Create frames and labels in left_frame 
        Label(top_frame, text="Session Code: ").grid(row=0, column=0)
        t = Text(top_frame,height=1,width=10)
        t.insert('end', self.key)
        t.configure(state='disabled')
        t.grid(row=0, column=1)
        

        Button(top_frame, text="Pen Color",command=self.change_fg,width=8).grid(row=1, column=0)

        Button(top_frame, text="BG Color",command=self.change_bg).grid(row=1, column=1)

        Button(top_frame, text="Clear",command=self.clear).grid(row=1, column=2)

        Label(top_frame, text='SHAPES:').grid(row=1,column=3,padx= 10)

        Button(top_frame, text="Circle",command= lambda: self.set_drawType("Circle")).grid(row=1, column=4)

        Button(top_frame, text="Rect",command= lambda: self.set_drawType("Rect")).grid(row=1, column=5)

        Button(top_frame, text="Pen",command=lambda: self.set_drawType("Pen")).grid(row=1, column=6)

        Button(top_frame, text="Line",command= lambda: self.set_drawType("Line")).grid(row=1, column=7)

        myfont = font.Font(overstrike = 1,size=10)
        shapeFill_btn =Button(top_frame, text="Fill",bg = 'light grey',font=myfont)
        shapeFill_btn.config(command=lambda : self.shapeFill(shapeFill_btn))
        shapeFill_btn.grid(row=1, column=8,padx=5)        

        Label(top_frame, text='Pen Width:').grid(row=1,column=9,padx= 5)
        self.slider = ttk.Scale(top_frame,from_= 5, to = 100,command=self.changeW,orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=1,column=10,ipadx=10,padx=5)

        
        Button(top_frame, text="Save",command= self.save_canvas).grid(row=1, column=12,padx=5)
            
            
        # Display canvas in right_frame
        self.c = Canvas(bottom_frame,width=500,height=500,bg=self.color_bg,)
        self.c.grid(row=0,column=0, padx=5, pady=5)
