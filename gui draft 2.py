# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:38:06 2024

@author: goconnor
"""

from tkinter import *

master = Tk()

# Set the geometry of tkinter frame
master.geometry("200x400")

# Set the Title of Tkinter window
master.title(" Project Parameter GUI ")

# Dictionary to store Entry widgets
entries = {}


def save_and_display():
    global entries
    data = {
        "Amplitude 1": float(e1.get()),
        "Frequency 1": float(e2.get()),
        "Amplitude 2": float(e3.get()),
        "Frequency 2": float(e4.get()),
        "Channel 1": float(e5.get()),
        "Channel 2": float(e6.get()),
        "Channel 3": float(e7.get()),
        "Channel 4": float(e8.get()),
        "pulse trigger": float(e9.get()),
    }

    for key, value in data.items():
        print(key + ": " + str(value))
        
        # Save the value in the global namespace
        globals()[key.replace(" ", "_").lower()] = value 
        #Using lower case and replacing space with underscore
        #e.g amplitude_1 , channel_1 , channel_2 , pulse_trigger
    return data


Label(master, text='Red Pitaya Inputs', fg='red').grid(row=0, columnspan=3)

Label(master, text='Output DAC 1').grid(row=1, columnspan=3)

Label(master, text='Amplitude 1').grid(row=2)
Label(master, text='Frequency 1').grid(row=3)

Label(master, text='Output DAC 2').grid(row=4, columnspan=3)

Label(master, text='Amplitude 2').grid(row=5)
Label(master, text='Frequency 2').grid(row=6)

Label(master, text='(Note: Freq < 62MHz, Amp < 1V)').grid(row=7, columnspan=3)

Label(master, text='Attenuator Values', fg='blue').grid(row=8, columnspan=3)
Label(master, text='Channel 1').grid(row=9)
Label(master, text='Channel 2').grid(row=10)
Label(master, text='Channel 3').grid(row=11)
Label(master, text='Channel 4').grid(row=12)

Label(master, text='(Note: Attenuator 0-95dB)').grid(row=13, columnspan=3)

Label(master, text='Other parameters').grid(row=14, columnspan=3)
Label(master, text='Pulse Trigger').grid(row=15)

Label(master, text='').grid(row=16, columnspan=3)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)

e1.grid(row=2, column=1)
e2.grid(row=3, column=1)
e3.grid(row=5, column=1)
e4.grid(row=6, column=1)
e5.grid(row=9, column=1)
e6.grid(row=10, column=1)
e7.grid(row=11, column=1)
e8.grid(row=12, column=1)
e9.grid(row=15, column=1)

# Button to save and display entered text
Button(master, text='Save and Display', command=save_and_display).grid(row=17, columnspan=2)

mainloop()

