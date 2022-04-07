import tkinter as tk
#Import tkinter library
from tkinter import *
from tkinter import ttk
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Define a new function to open the window

def temp_win():
   temp = Toplevel(win)
   temp.geometry("750x250")
   temp.title("Temperature")
   #Create a Label in New window
   #Label(new, text="What would you like the minimum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)

   Label(temp, text="What would you like the maximum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(temp, text="Change Max Temp", command=Temp).pack()
   Label(temp, text="What would you like the minimum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(temp, text="Change Min Temp", command=Temp).pack()
   
class Temp:
    def __init__ (self):
        temp_win()
        self.root = tk.Tk()

        self.slider = tk.Scale(self.root, from_=0, to=256, 
                               orient="horizontal")
        self.slider.bind("<ButtonRelease-1>", self.updateValue)
        self.slider.pack()
        self.root.mainloop()

    def updateValue(self, event):
        print (self.slider.get())
temp = Temp()




