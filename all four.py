# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:15:18 2024

@author: goconnor
"""
#below is for the channels on attenuator 

from tkinter import *
import requests


def save_data():
    attenuation_values = {
        'att1': float(att1.get()),
        'att2': float(att2.get()),
        'att3': float(att3.get()),
        'att4': float(att4.get())
    }
    for att, value in attenuation_values.items():
        requests.get(f'http://192.168.1.11/:CHAN:{att[-1]}:SETATT:{value}\n')
        #not a static ip change to ip 
   
    
   
window = Tk()
window.geometry("190x155")
window.title("Project Parameter GUI")

Label(window, text='Attenuator Values ', fg='blue').grid(row=2, columnspan=3)



# Label and Entry for attenuation 4
label_att1 = Label(window, text="Channel 1:")
label_att1.grid(row=3)
att1 = StringVar()
att1.set("0")
a1 = Entry(window, textvariable=att1)
a1.grid(row=3,column=2)

label_att2 = Label(window, text="Channel 2:")
label_att2.grid(row=4)
att2 = StringVar()
att2.set("0")
a2 = Entry(window, textvariable=att2)
a2.grid(row=4,column=2)

label_att3 = Label(window, text="Channel 3:")
label_att3.grid(row=5)
att3 = StringVar()
att3.set("0")
a3 = Entry(window, textvariable=att3)
a3.grid(row=5,column=2)

label_att4 = Label(window, text="Channel 4:")
label_att4.grid(row=6)
att4 = StringVar()
att4.set("0")
a4 = Entry(window, textvariable=att4)
a4.grid(row=6,column=2)

Label(window, text='(Note: Attenuator 0-95dB)',fg='red').grid(row=7, columnspan=3)

save_button = Button(window, text="Save Attenuations",fg='green', command=save_data)
save_button.grid(row=8, columnspan=3)

window.mainloop()
