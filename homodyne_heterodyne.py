# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:49:15 2024

@author: garyo
"""
#this code was developed by Dr.Colm Bracken for use in Third Year labs to 
#introduce students to homodyne/heterodyne techniques

import numpy as np
import matplotlib.pyplot as plt

#Homodyne mixing
f_RF=2e6
f_LO=2e6

#Heterodyne mixing
#f_RF=2e6
#f_RF=2.2e6

def V(a,f,t): #a is amplitude f frequency t is the time
    return a*np.sin(2*np.pi*f*t)

num=5000
maxt=0.00006
tt=np.linspace(0,maxt,num)
Vout=(V(1.0,f_RF,tt)+V(1.0,f_LO,tt))**2 #output from mixer

fig = plt.figure(figsize=(20,2))
ax = fig.add_subplot(111)
ax.plot(tt,Vout)
plt.xlabel('time (s) ', fontsize=14)
plt.ylabel('signal (arb units)',fontsize=14)
plt.show()

fftVout=np.zeros(num, dtype='complex128')
fftVout=np.fft.fft(Vout)
freq = np.fft.fftfreq(Vout.size,d=tt[1]-tt[0])

fig = plt.figure(figsize=(20,2)) #plot the frequency spectrum
ax = fig.add_subplot(111)
ax.plot(freq,abs(fftVout))
ax.plot([f_RF-f_LO,f_RF-f_LO],[0,max(abs(fftVout))],'C1--')
ax.plot([f_RF+f_LO,f_RF+f_LO],[0,max(abs(fftVout))],'C1--')
ax.plot([2*f_RF,2*f_RF],[0,max(abs(fftVout))],'C2--')
ax.plot([2*f_LO,2*f_LO],[0,max(abs(fftVout))],'C2--')
plt.xlabel('frequency (Hz)')
plt.ylabel('response (arb. units)')
plt.text((f_RF-f_LO)*1.01,max(abs(fftVout))/2,'%.3e Hz\n f_IF' % (f_RF-f_LO),color='C1')
plt.text((f_RF+f_LO)*1.01,max(abs(fftVout))/2,'%.3e Hz' % (f_RF+f_LO),color='C1')
plt.text((2*f_RF)*1.01,max(abs(fftVout))/2,'%.3e Hz\n 2*f_RF' % (2*f_RF),color='C2')
plt.text((2*f_LO)*1.01,max(abs(fftVout))/2,'%.3e Hz\n 2*f_LO' % (2*f_LO),color='C2')


#plt.legend()
plt.xlim([0,6e6])