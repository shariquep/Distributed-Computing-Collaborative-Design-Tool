from tkinter import *

def pencilLine(gui, params):
    if "x" in params and "y" in params:
        x = params["x"]
        y = params["y"]
        width = params["width"]
        col = params["outline"]
        for i in range(1,len(x)):
            gui.c.create_line(x[i-1],y[i-1],x[i],y[i],width=width,fill=col,capstyle=ROUND,smooth=True)

def erase(gui, params):
    if "x" in params and "y" in params:
        x = params["x"]
        y = params["y"]
        width = params["width"]
        col = params["background"]
        for i in range(1,len(x)):
            line = gui.c.create_line(x[i-1],y[i-1],x[i],y[i],width=width,fill=col,capstyle=ROUND,smooth=True)
            gui.erased.append(line)

def clearCanvas(gui, params):
    gui.erased = []
    gui.c.delete(ALL)

def changeBG(gui, params):
    for line in gui.erased:
        if line == None:
            continue

        gui.c.itemconfig(line,fill=params["bg"])

    gui.c['bg'] = params["bg"]

def drawRectangle(gui, params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["fill"]
    outline = params["outline"]
    gui.c.create_rectangle(x1,y1,x2,y2,width=width,outline=outline,fill=col)

def drawCircle(gui, params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["fill"]
    outline = params["outline"]
    gui.c.create_oval(x1,y1,x2,y2,width=width,outline=outline,fill=col)

def straightLine(gui, params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["outline"]
    gui.c.create_line(x1,y1,x2,y2,width=width,fill=col,capstyle=ROUND,smooth=True)

def changePermission(gui, params):
    gui.permission = params["access"] == 1


def drawPencil(old_x,old_y,e,width,col,params,canvas):
    line = None
    if old_x and old_y:
            line = canvas.create_line(old_x,old_y,e.x,e.y,width=width,fill=col,capstyle=ROUND,smooth=True)

    old_x = e.x
    old_y = e.y
    
    if "x" in params:
        params["x"].append(old_x)
    else:        
        params["x"] = [old_x]
    
    if "y" in params:
        params["y"].append(old_y)
    else:        
        params["y"] = [old_y]
    
    return old_x,old_y,params,line

    
