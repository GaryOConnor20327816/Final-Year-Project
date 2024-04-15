# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:10:06 2024

@author: goconnor
Code for use on Red Pitaya
"""

import time
import numpy as np
from matplotlib import pyplot as plt
from rp_overlay import overlay
import rp

fpga = overlay()
rp.rp_Init()

#-----------------------------------------------------Attenuator--------------------------------------------------------------------------#
"""
import requests

x = requests.get('http://192.168.1.11/ATT?\n')

attenuation_value1 = float(input('Enter value for channel 1 (0-95dB): '))
attenuation_value2 = float(input('Enter value for channel 2 (0-95dB): '))
attenuation_value3 = float(input('Enter value for channel 3 (0-95dB): '))
attenuation_value4 = float(input('Enter value for channel 4 (0-95dB): '))

if(0<=attenuation_value1<95):
    C1= requests.get(f'http://192.168.1.11/:CHAN:1:SETATT:{attenuation_value1}\n')
if(0<=attenuation_value2<95):
    C2= requests.get(f'http://192.168.1.11/:CHAN:2:SETATT:{attenuation_value2}\n')
if(0<=attenuation_value3<95): 
    C3= requests.get(f'http://192.168.1.11/:CHAN:3:SETATT:{attenuation_value3}\n')
if(0<=attenuation_value4<95):
    C4= requests.get(f'http://192.168.1.11/:CHAN:4:SETATT:{attenuation_value4}\n')
"""

#---------------------------------------------------------Red Pitaya--------------------------------------------------------------------------#

#Generator parameter

#output1
channel1 = rp.RP_CH_1
waveform1 = rp.RP_WAVEFORM_SINE
freq1 = 10e6 #max 60e6
ampl1 = .2 #max 1
#freq1 = float(input('Enter a value for Frequency 1 (0-60MHz): '))
#ampl1 = float(input('Enter a value for Amplitude 1 (0-1V): '))

#output2
channel2 = rp.RP_CH_2
waveform2 = rp.RP_WAVEFORM_SINE
freq2 = 15e6
ampl2 = 0.4
#freq2 = float(input('Enter a value for Frequency 2 (0-60MHz): '))
#ampl2 = float(input('Enter a value for Amplitude 2 (0-1V): '))

#----------------------------------------------------------------generating signal--------------------------------------------------------------#

# Acquisition paramters
dec = rp.RP_DEC_1

trig_lvl = 0.5
trig_dly = 0

acq_trig_sour = rp.RP_TRIG_SRC_NOW
N = 400 #after 16000 flatline


rp.rp_GenReset()
rp.rp_AcqReset()

print("Gen_start")

#wave from channel 1
rp.rp_GenWaveform(channel1, waveform1)
rp.rp_GenFreqDirect(channel1, freq1)
rp.rp_GenAmp(channel1, ampl1)

#wave from channel 2
rp.rp_GenWaveform(channel2, waveform2)
rp.rp_GenFreqDirect(channel2, freq2)
rp.rp_GenAmp(channel2, ampl2)

rp.rp_GenTriggerSource(channel1, rp.RP_GEN_TRIG_SRC_INTERNAL)

rp.rp_GenOutEnableSync(True)
rp.rp_GenSynchronise()

# Set Decimation
rp.rp_AcqSetDecimation(dec)

# Set trigger level and delay
rp.rp_AcqSetTriggerLevel(rp.RP_T_CH_1, trig_lvl)
rp.rp_AcqSetTriggerDelay(trig_dly)

#Input readings

# Start Acquisition
print("Acq_start")
rp.rp_AcqStart()

time.sleep(0.1)

# Specify trigger - immediately
rp.rp_AcqSetTriggerSrc(acq_trig_sour)

# Trigger state
while 1:
    trig_state = rp.rp_AcqGetTriggerState()[1]
    if trig_state == rp.RP_TRIG_STATE_TRIGGERED:
        break

# Fill state
while 1:
    if rp.rp_AcqGetBufferFillState()[1]:
        break


### Get data ###
# RAW
ibuff = rp.i16Buffer(N)
res = rp.rp_AcqGetOldestDataRaw(rp.RP_CH_1, N, ibuff.cast())[1]
#res02 = rp.rp_AcqGetOldestDataRaw(rp.RP_CH_2, N, ibuff.cast())[1]

# Volts
fbuff1 = rp.fBuffer(N)
res1 = rp.rp_AcqGetOldestDataV(rp.RP_CH_1, N, fbuff1)[1]
fbuff2 = rp.fBuffer(N)
res2 = rp.rp_AcqGetOldestDataV(rp.RP_CH_2, N, fbuff2)[1]

data_V1 = np.zeros(N, dtype = float)
data_V2 = np.zeros(N, dtype = float)
data_raw = np.zeros(N, dtype = int)
X = np.arange(0, N, 1)



for i in range(0, N, 1):
    data_V1[i] = fbuff1[i]
    data_V2[i] = fbuff2[i]
    data_raw[i] = ibuff[i]

#reading data to a file


# Format X, data_V1, and data_V2 arrays
formatted_X = ['{0:<10f}'.format(x) for x in X]
formatted_data_V1 = ['{0:<10f}'.format(v) for v in data_V1]
formatted_data_V2 = ['{0:<10f}'.format(v) for v in data_V2]

# Convert formatted data back to numerical arrays
formatted_X = np.array(formatted_X)
formatted_data_V1 = np.array(formatted_data_V1)
formatted_data_V2 = np.array(formatted_data_V2)

# Stack the formatted arrays horizontally
data1 = np.column_stack((formatted_X, formatted_data_V1))
data2 = np.column_stack((formatted_X, formatted_data_V2))


header1 = "samples     voltage(V)"
header2 = "samples     voltage(V)"

# Save data_V1 to a file
np.savetxt('data_V1.txt', data1, header=header1, comments='', fmt='%s')

# Save data_V2 to a file
np.savetxt('data_V2.txt', data2, header=header2, comments='', fmt='%s')


#plotting data
#figure, axis = plt.subplots(2,1,constrained_layout = True) 
#axis[0].plot(X, data_V1) 
#axis[0].set_title("waveform input 1",color='red')
#axis[0].set_xlabel('number of samples')
#axis[0].set_ylabel('Volts')
#axis[0].grid(True)

#axis[1].plot(X, data_V2) 
#axis[1].set_title("waveform input 2",color='red')
#axis[1].set_xlabel('number of samples')
#axis[1].set_ylabel('Volts')
#axis[1].grid(True)

plt.figure(figsize=(10, 6))
plt.plot(X, data_V1) 
plt.title("waveform input 1",color='red')
plt.xlabel('number of samples')
plt.ylabel('Volts')
plt.grid(True)

#-------------------------------------------------------frequency spectrum---------------------------------------------------------------------------#

# Read data from file
file_path = "data_V1.txt"
data = np.loadtxt(file_path, skiprows=1)

# Extract voltage values from the right side of the data array
voltages = data[:, 1]  # Assuming the voltage values are in the second column

# Number of samples
#num_samples = 100

# Sampling frequency
fs = N / (data[-1, 0] - data[0, 0])  # Assuming time values are in the first column

# Compute FFT
fft_result = np.fft.fft(voltages)
freq = np.fft.fftfreq(N, 1/fs)  # Frequency bins

# Scale the x-axis
freq_scaled = freq * (12.5 / 0.1)


# Convert magnitude (yaxis) to decibels
magnitude_dB = 20 * np.log10(np.abs(fft_result) + 1e-10) - 40  # Adding a small constant to prevent division by zero
                                                               # 40 shift to line up with expected from Red Pitaya

plt.figure(figsize=(10, 6))
plt.plot(freq_scaled[:len(freq_scaled)//2], magnitude_dB[:len(freq_scaled)//2])  # Plot only positive frequencies
plt.title('Frequency Spectrum Input 1 in Db')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()

# Save the frequency spectrum data to a file
power_spectrum_data1 = np.column_stack((freq_scaled[:len(freq_scaled)//2], magnitude_dB[:len(freq_scaled)//2]))
header_power_spectrum1 = "Frequency (MHz) Magnitude (dB)"
np.savetxt('powerspectrumDb.txt', power_spectrum_data1, header=header_power_spectrum1, comments='', fmt='%f')

plt.figure(figsize=(10, 6))
plt.plot(freq_scaled[:len(freq_scaled)//2], np.abs(fft_result)[:len(freq_scaled)//2])  # Plot only positive frequencies
plt.title('Frequency Spectrum input 1, main frequency(s)')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()

# Save the frequency spectrum data to a file
power_spectrum_data = np.column_stack((freq_scaled[:len(freq_scaled)//2], np.abs(fft_result)[:len(freq_scaled)//2]))
header_power_spectrum = "Frequency (MHz) Magnitude"
np.savetxt('powerspectrum.txt', power_spectrum_data, header=header_power_spectrum, comments='', fmt='%f')


#-------------------------------------------------------------IQ Plane------------------------------------------------------------------------------#

# Load frequency spectrum data
power_spectrum_data = np.loadtxt('powerspectrum.txt', skiprows=1)
freq_scaled = power_spectrum_data[:, 0]
magnitude = power_spectrum_data[:, 1]

# Find the indices of the two highest spikes
sorted_indices = np.argsort(magnitude)
top_indices = sorted_indices[-2:]  # Get the indices of the two highest spikes

# Get the frequencies corresponding to the two highest spikes
freq1 = freq_scaled[top_indices[0]]
freq2 = freq_scaled[top_indices[1]]

num_samples = N  # Number of samples

# Generate time array
t = np.linspace(0, 1, num_samples)

# Generate complex sinusoidal signals for the two frequencies
complex_signal1 = ampl1 * np.exp(2j * np.pi * freq1 * t)
complex_signal2 = ampl1 * np.exp(2j * np.pi * freq2 * t)

# Extract I and Q components for the two channels
I1 = np.real(complex_signal1)
Q1 = np.imag(complex_signal1)
I2 = np.real(complex_signal2)
Q2 = np.imag(complex_signal2)

# Plot the IQ plane for the two frequencies
plt.figure(figsize=(8, 6))
plt.scatter(I1, Q1, color='blue', s=5, label=f'Freq={freq1}, Amp={ampl1}')
plt.scatter(I2, Q2, color='green', s=5, label=f'Freq={freq2}, Amp={ampl2}')
plt.title('IQ Plane for input 1')
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.axis('equal')
plt.legend()
plt.show()

#above code can be copied and pasted for output2 as only require one input for the readout system only need once


#axis[2].plot(X, data_raw) 
#axis[2].set_title("RAW") 
#axis[2].set_xlabel('number of samples')
#axis[2].set_ylabel('bits?')
#axis[2].grid(True)
#plt.show()

# Release resources
rp.rp_Release()