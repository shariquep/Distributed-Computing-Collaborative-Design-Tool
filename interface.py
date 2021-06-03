from PIL import Image, ImageTk
import tkinter as tk
import paint


name=''
code = ''
request_type=''

def newSession(e1,root):
    global name,request_type
    name = e1.get()
    request_type="create"
    print("New session")
    root.destroy()

def existingSession(e1,e2,root):
    global code,name,request_type
    name = e1.get()
    code = e2.get()
    request_type="join"
    root.destroy()

def startPaint():

        print("Paint started")
        root = tk.Tk()
        paint.main(root)
        root.title('Paint App')
        root.mainloop()
        
def display():

    bgColor= '#FAFAF0'

    root = tk.Tk()

    root.title('Paint App')
    root.configure(bg=bgColor)

    #load logo image
    image = Image.open('./logo2.png')
    image = image.resize((450, 150), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(image)
    logoLBL = tk.Label(image = logo)

    # Create Frame widgets for whitespace
    left_frame = tk.Frame(root, width=150, height=500,bg=bgColor)
    left_frame.grid(row=0, column=0)

    center_frame = tk.Frame(root, width=300, height=300,bg=bgColor)
    center_frame.grid(row=0, column=1, padx=10, pady=5)

    right_frame = tk.Frame(root, width=150, height=500,bg=bgColor)
    right_frame.grid(row=0, column=2)

    mini_frame = tk.Frame(center_frame, width=250, height=200,bg=bgColor,pady=20)

    #Add logo
    logoLBL =tk.Label(center_frame,image=logo)
    logoLBL.image = logo
    logoLBL.grid(columnspan=5,padx=20,pady=30)

    #Frame for name input widgets
    tk.Label(center_frame,text="",bg=bgColor,width=10).grid(row=1,column=0)
    l1=tk.Label(center_frame,text="Enter name:",bg=bgColor,width=15,font=('Calibri', 14 )).grid(row=1,column=1)
    e1 = tk.Entry(center_frame,font=('Calibri', 14 ))
    e1.grid(row=1,column=2)
    tk.Label(center_frame,text="",bg=bgColor,width=10).grid(row=1,column=4)

    #Frame for New Session widgets
    mini_frame.grid(row=2,column=1,columnspan=2)
    btn1=tk.Button(mini_frame,text="New Session",background="#004E89",fg="white",width=20,font=('Calibri', 14, ), command=lambda: newSession(e1,root)).pack(fill='x')
    l2=tk.Label(mini_frame,text="OR",bg=bgColor,font=('Calibri', 18 )).pack(pady=5)

    #Frame for join Session widgets
    l3=tk.Label(center_frame,text="Enter code of existing session:",bg=bgColor,font=('Calibri', 14 )).grid(row=4,column=1)
    e2 = tk.Entry(center_frame,font=('Calibri', 14 ))
    e2.grid(row=4,column=2)
    btn2=tk.Button(center_frame,text="Join",font=('Calibri', 14 ),bg="#004E89",fg="white", command=lambda: existingSession(e1,e2,root)).grid(row=4,column=3,padx=8)

    root.mainloop()
    return name,request_type,code
