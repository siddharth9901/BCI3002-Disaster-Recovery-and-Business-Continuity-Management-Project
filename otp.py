from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import hashlib #for sha512 function
import time

# from tkinter import ttk
from tkinter import * #for gui

def generateOTP():
    secret = open('key.txt').read().strip()
    matrix = list()
    temp = list(secret)
    row = list()
    for i in range(0, len(temp), 2):
        temp2 = secret[i] + secret[i + 1]
        row.append(temp2)
        if (len(row) == 8):
            matrix.append(row)
            row = []
    currenttime = int(time.time()) // 100
    row = (currenttime // 3) % 8
    column = (currenttime // 5) % 8
    otp = matrix[row][column] + str(currenttime)
    otp = int(hashlib.sha512(otp.strip().encode('utf-8')).hexdigest(), 16) % 1000000
    print(" OTP : ", otp)
    global OTP
    OTP.configure(text=str(otp))

def saveKey():
    file=open('key.txt', 'w')
    file.write(key_input.get(1.0,END).strip() )
    file.close()
    return


root = Tk()
root.title("OTP Generator")
root.geometry("550x400")
# root.configure(bg='white')
s = ttk.Style(root)
s.configure("TNotebook", tabposition='n',background='#6C6C6C')
s.configure("TFrame",background='#FAEBD7')
notebook = ttk.Notebook(root,padding=20);
notebook.pack(expand=1, fill="both")
frame1 = ttk.Frame(notebook,relief=GROOVE,padding=10)
frame2 = ttk.Frame(notebook,relief=GROOVE,padding=10)
frame3 = ttk.Frame(notebook,relief=GROOVE,padding=10)
notebook.add(frame1, text='   Generate OTP   ')
notebook.add(frame2, text='   Settings   ')
notebook.add(frame3, text='   About   ')
Generate_OTP_Label=Label(frame1,text="  Generate OTP: ",font=('Arial', 14, 'bold'),background='#FAEBD7')
Generate_OTP_Label.grid(padx=5,pady=10,row=0,column=0)
OTP = Label(frame1,text="",font=('Arial', 12),background='#FAEBD7')
OTP.grid(padx=5,pady=10,row=2, column=2,rowspan=3)
Gen_OTP_Button=Button(frame1,text = " Generate OTP ",font=('Arial', 12),activebackground='LightSeaGreen',background='LightSkyBlue',relief=FLAT,command=generateOTP)
Gen_OTP_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=5,column=2,sticky='S')


Label(frame2,text="Settings:                                                          ",font=('Arial', 14, 'bold'),background='#FAEBD7').grid(padx=5,pady=10,row=0,column=0,sticky="E")
msg=StringVar(frame2,"")
Label(frame2,text="Enter Secret Key:                                                              ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=1,column=0, sticky="E")
key_input=ScrolledText(frame2,width=50,height=5)
key_input.grid(padx=50,pady=10,row=3, column=0,columnspan=5,sticky="W")
Save_Button=Button(frame2,text = " Save Key ",font=('Arial', 12),activebackground='Coral',background='LightSeaGreen',relief=FLAT,command=saveKey)
Save_Button.grid(ipadx=10,ipady=10,padx=50,pady=10,row=4,column=0,sticky="W")



Label(frame3,text=" About: ",font=('Arial', 14, 'bold'),background='#FAEBD7').grid(padx=5,pady=10,row=0,column=0,sticky='W')
Label(frame3,text=" Version: 1",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=1,column=0,sticky='W')
Label(frame3,text=" This Application Was Created By ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=2,column=0,sticky='W')
Label(frame3,text=" Vasu Mandhanya 19BCI0161",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=3,column=0,sticky='W')
Label(frame3,text=" Siddharth Dinkar 19BCI0122",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=4,column=0,sticky='W')
Label(frame3,text=" Yuvraj Singh Pathania 19BCE0561 ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=5,column=0,sticky='W')
root.mainloop()