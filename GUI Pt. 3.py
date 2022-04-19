#Import tkinter library
from tkinter import *
from tkinter import ttk
import time
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Define a new function to open the window

global maxtempslider
global mintempslider
global maxhumslider
global minhumslider
global max_temp
global min_temp
global max_hum
global min_hum

def temp_win():
   temp = Toplevel(win)
   temp.geometry("750x250")
   temp.title("Temperature")
   #Create a Label in New window
   #Label(new, text="What would you like the minimum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)

   Label(temp, text="What would you like the maximum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(temp, text="Change Max Temp", command=max_temp_slider).pack()
   Label(temp, text="What would you like the minimum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(temp, text="Change Min Temp", command=min_temp_slider).pack()


def max_temp_slider():
   global maxtempslider
   temps = Toplevel(win)
   win.geometry('750x250')
   win.title('Temperature Slider')
   maxtempslider = Scale(temps, from_=0, to=150)
   maxtempslider.pack()
   max_temp = maxtempslider.get()
   ttk.Button(temps, text = "Confirm new Temp", command = set_max_temp).pack()
   max_temp = maxtempslider.get()
   maxtempslider.set(max_temp)


def set_max_temp():
   max_temp = maxtempslider.get()
   #maxtempslider.set(maxtemp)
   print(maxtempslider.get())
   print("New max temp is: ", max_temp)
   maxtempslider.destroy()
   #win(Toplevel).destroy()

def min_temp_slider():
   global mintempslider
   temps = Toplevel(win)
   win.geometry('750x250')
   win.title('Temperature Slider')
   mintempslider = Scale(temps, from_=0, to=150)
   mintempslider.pack()
   ttk.Button(temps, text = "Confirm new Temp", command = set_min_temp).pack()
   min_temp = mintempslider.get()
   mintempslider.set(min_temp)
   
def set_min_temp():
   min_temp = mintempslider.get()
   #mintempslider.set(min_temp)
   print('New min temp is: ', min_temp)
   
def hum_win():
   hum= Toplevel(win)
   hum.geometry("750x250")
   hum.title("Humidity")
   #Create a Label in New window
   Label(hum, text="What would you like the minimum humidity percentage to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(hum, text="Change Min Humidity Percentage", command=min_hum_slider).pack()
   Label(hum, text="What would you like the maximum humidity percentage to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(hum, text="Change Max Humidity Percentage", command=max_hum_slider).pack()

def min_hum_slider():
   global minhumslider
   hums = Toplevel(win)
   win.geometry('750x250')
   win.title('Humidity Slider')
   minhumslider = Scale(hums, from_=0, to=100)
   minhumslider.pack()
   ttk.Button(hums, text = "Confirm new humidity level", command = set_min_hum).pack()
   min_hum = minhumslider.get()
   minhumslider.set(min_hum)
   
def set_min_hum():
   min_hum = minhumslider.get()
   #mintempslider.set(min_temp)
   print('New min temp is: ', min_hum)
   
def max_hum_slider():
   global maxhumslider
   hums = Toplevel(win)
   win.geometry('750x250')
   win.title('Humidity Slider')
   maxhumslider = Scale(hums, from_=0, to=100)
   maxhumslider.pack()
   ttk.Button(hums, text = "Confirm new humidity level", command = set_max_hum).pack()
   max_hum = max_hum_slider.get()

def set_max_hum():
   max_hum = maxhumslider.get()
   #mintempslider.set(min_temp)
   print('New max hum is: ', max_temp)
   return max_temp
   
def soil_win():
   soil= Toplevel(win)
   soil.geometry("750x250")
   soil.title("Soil")
   #Create a Label in New window
   Label(soil, text="Buncha soil stuff I have to figure out units for", font=('Helvetica 17 bold')).pack(pady=30)

#Create a label
Label(win, text= "Which subsystem would you like to view?", font= ('Helvetica 17 bold')).pack(pady=30)
#Create a button to open a New Window
ttk.Button(win, text="Temperature", command=temp_win).pack()
ttk.Button(win, text="Humidity", command=hum_win).pack()
ttk.Button(win, text="Soil Levels", command=soil_win).pack()

win.mainloop()
print("Is it running")
