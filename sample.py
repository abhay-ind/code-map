from tkinter import *
from tkinter import messagebox
top=Tk()
top.geometry("400x400")

def helloCallBack():
	msg=messagebox.showinfo("Java Control Flow","Let's make a wonderful app")

B=Button(top,text="Let's Flow", command=helloCallBack)
B.place(x=150,y=150)

top.mainloop()