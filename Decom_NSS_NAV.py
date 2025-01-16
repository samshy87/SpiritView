
# Opens a file dialog to allow a user to select a .c10 file, 
# then decoms the data and creates an output CSV file in the 
# same location the selected C10 file lives

import os
import csv
import tkinter as tk
from chapter10 import C10
from Number_Conversions import float_1750A_32bit_toDecimal
from math import pi
from tqdm import *
from tkinter import filedialog

# variable to convert radians to decimal degrees
radToDecDeg = 180/pi
# opens file dialog to select .c10
root = tk.Tk()
root.withdraw()
fileName = filedialog.askopenfilename()
# output file
outputFile = fileName[:-4] + "_NSS_Nav.csv"
# progress bar variable
fileSize = os.path.getsize(fileName)

# create output CSV with headers
nssHeaders = ['Time','Latitude','Longitude','Altitude','NSS R1 Velocity','NSS R2 Velocity','NSS R3 Velocity','True Heading', 'True Track', 'Ground Speed', 'NSS Roll', 'NSS Pitch']
with open(outputFile,'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(nssHeaders)

# set up progress bar
with tqdm(total=fileSize, ncols=100, colour='blue') as progressBar:
    # loop through each packet in C10 file 
    for packet in C10(fileName):
        # update progress bar
        progressBar.update(packet.packet_length)
        # find all 1553 messages in a file
        if packet.data_type == 0x19:
            for msg in packet:
                # ***** Nav Message ********************************************************************************************
                if msg.data[0] == 96 and msg.data[1] == 34:
                    
                    latitude = msg.data[6]
                    latitude = (latitude << 8) + msg.data[5]
                    latitude = (latitude << 8) + msg.data[8]
                    latitude = (latitude << 8) + msg.data[7]
                    latitude = float_1750A_32bit_toDecimal(latitude)*radToDecDeg
                    
                    longitude = msg.data[10]
                    longitude = (longitude << 8) + msg.data[9]
                    longitude = (longitude << 8) + msg.data[12]
                    longitude = (longitude << 8) + msg.data[11]
                    longitude = float_1750A_32bit_toDecimal(longitude)*radToDecDeg
                    
                    altitude = msg.data[14]
                    altitude = (altitude << 8) + msg.data[13]
                    altitude = (altitude << 8) + msg.data[16]
                    altitude = (altitude << 8) + msg.data[15]
                    altitude = float_1750A_32bit_toDecimal(altitude)
                    
                    nssR1 = msg.data[18]
                    nssR1 = (nssR1 << 8) + msg.data[17]
                    nssR1 = (nssR1 << 8) + msg.data[20]
                    nssR1 = (nssR1 << 8) + msg.data[19]
                    nssR1 = float_1750A_32bit_toDecimal(nssR1)
                    
                    nssR2 = msg.data[22]
                    nssR2 = (nssR2 << 8) + msg.data[21]
                    nssR2 = (nssR2 << 8) + msg.data[24]
                    nssR2 = (nssR2 << 8) + msg.data[23]
                    nssR2 = float_1750A_32bit_toDecimal(nssR2)
                    
                    nssR3 = msg.data[26]
                    nssR3 = (nssR3 << 8) + msg.data[25]
                    nssR3 = (nssR3 << 8) + msg.data[28]
                    nssR3 = (nssR3 << 8) + msg.data[27]
                    nssR3 = float_1750A_32bit_toDecimal(nssR3)    
                    
                    trueHeading = msg.data[34]
                    trueHeading = (trueHeading << 8) + msg.data[33]
                    trueHeading = (trueHeading << 8) + msg.data[36]
                    trueHeading = (trueHeading << 8) + msg.data[35]
                    trueHeading = float_1750A_32bit_toDecimal(trueHeading)
                    
                    trueTrack = msg.data[38]
                    trueTrack = (trueTrack << 8) + msg.data[37]
                    trueTrack = (trueTrack << 8) + msg.data[40]
                    trueTrack = (trueTrack << 8) + msg.data[39]
                    trueTrack = float_1750A_32bit_toDecimal(trueTrack)
                    
                    groundSpeed = msg.data[42]
                    groundSpeed = (groundSpeed << 8) + msg.data[41]
                    groundSpeed = (groundSpeed << 8) + msg.data[44]
                    groundSpeed = (groundSpeed << 8) + msg.data[43]
                    groundSpeed = float_1750A_32bit_toDecimal(groundSpeed)
                    
                    nssRoll = msg.data[50]
                    nssRoll = (nssRoll << 8) + msg.data[49]
                    nssRoll = (nssRoll << 8) + msg.data[52]
                    nssRoll = (nssRoll << 8) + msg.data[51]
                    nssRoll = float_1750A_32bit_toDecimal(nssRoll)
                    
                    nssPitch = msg.data[54]
                    nssPitch = (nssPitch << 8) + msg.data[53]
                    nssPitch = (nssPitch << 8) + msg.data[56]
                    nssPitch = (nssPitch << 8) + msg.data[55]
                    nssPitch = float_1750A_32bit_toDecimal(nssPitch)
                    
                    # append message to CSV file
                    csvRow = [msg.get_time(),latitude,longitude,altitude,nssR1,nssR2,nssR3,trueHeading,trueTrack,groundSpeed,nssRoll,nssPitch]
                    with open(outputFile,'a',newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(csvRow)
                # ***** End Nav Message ****************************************************************************************

                    
        