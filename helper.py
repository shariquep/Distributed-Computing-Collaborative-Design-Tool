from tkinter import *

def pencilLine(canvas, params):
    if "x" in params and "y" in params:
        x = params["x"]
        y = params["y"]
        width = params["width"]
        col = params["outline"]
        for i in range(1,len(x)):
            canvas.create_line(x[i-1],y[i-1],x[i],y[i],width=width,fill=col,capstyle=ROUND,smooth=True)

def clearCanvas(canvas,params):
    canvas.delete(ALL)

def changeBG(canvas,params):
    canvas['bg'] = params["bg"]    

def drawRectangle(canvas,params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["fill"]
    outline = params["outline"]
    canvas.create_rectangle(x1,y1,x2,y2,width=width,outline=outline,fill=col)

def drawCircle(canvas,params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["fill"]
    outline = params["outline"]
    canvas.create_oval(x1,y1,x2,y2,width=width,outline=outline,fill=col)

def straightLine(canvas,params):
    x1 = params["x1"]
    y1 = params["y1"]
    x2 = params["x2"]
    y2 = params["y2"]
    width = params["width"]
    col = params["fill"]
    canvas.create_line(x1,y1,x2,y2,width=width,fill=col,capstyle=ROUND,smooth=True)

def drawPencil(old_x,old_y,e,width,col,params,canvas):
    if old_x and old_y:
            canvas.create_line(old_x,old_y,e.x,e.y,width=width,fill=col,capstyle=ROUND,smooth=True)

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
    
    return old_x,old_y,params

    
