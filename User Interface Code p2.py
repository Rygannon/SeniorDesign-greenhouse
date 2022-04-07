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
   ttk.Button(temp, text="Change Max Temp", command=max_temp_slider).pack()
   Label(temp, text="What would you like the minimum temperature to be?", font=('Helvetica 17 bold')).pack(pady=30)
   ttk.Button(temp, text="Change Min Temp", command=min_temp_slider).pack()


global max_temp
global min_temp

def max_temp_slider():   
   temps = Toplevel(win)
   win.geometry('750x250')
   win.title('Temperature Slider')
   ttk.Button(temps, text = "Confirm new Temp", command = set_max_temp).pack()
   global maxtempslider
   maxtempslider = Scale(temps, from_=0, to=150)
   maxtempslider.set(max_temp)
   maxtempslider.pack()
   max_temp = maxtempslider.get()
   def __init__(self):
      self.root = tk.Tk()
      self.slider = tk.Scale(self.root, from_=0, to=256, orient="horizontal")
      self.slider.bind("<ButtonRelease-1>", self.set_max_temp)
      self.slider.pack()
      self.root.mainloop()
      print (self.maxtempslider.get())
      maxtemp = maxtempslider.get()
      print('Current Max Temp is:', maxtemp)

def set_max_temp():
   maxtempslider.set(maxtemp)
   print(maxtempslider.get())

def min_temp_slider():
   global mintempslider
   temps = Toplevel(win)
   win.geometry('750x250')
   win.title('Temperature Slider')
   ttk.Button(temps, text = "Confirm new Temp", command = set_min_temp).pack()
   mintempslider = Scale(temps, from_=0, to=150)
   #mintempslider.set(min_temp)
   mintempslider.pack()
   min_temp = mintempslider.get()
   print('Current Min Temp is: ', min_temp)
   
def set_min_temp():
   mintempslider.set(min_temp)
   print(min_temp)
   
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
   hums = Toplevel(win)
   win.geometry('750x250')
   win.title('Humidity Slider')
   humslider = Scale(hums, from_=0, to=100)
   humslider.pack()
   min_hum = min_hum_slider.get()

def max_hum_slider():
   hums = Toplevel(win)
   win.geometry('750x250')
   win.title('Humidity Slider')
   humslider = Scale(hums, from_=0, to=100)
   humslider.pack()
   max_hum = max_hum_slider.get()

   
   print('Current Min Temp is:', min_temp)
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
#maxtempslider.set(max_temp)
