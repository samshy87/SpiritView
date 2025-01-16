
# Opens a file dialog to allow a user to select a .c10 file, 
# then decoms the data and creates an output CSV file in the 
# same location the selected C10 file lives

import os
import csv
import tkinter as tk
from chapter10 import C10
from tqdm import *
from tkinter import filedialog

# opens file dialog to select .c10
root = tk.Tk()
root.withdraw()
fileName = filedialog.askopenfilename()
# output file
outputFile = fileName[:-4] + "_BAY_LNCHR.csv"
# progress bar variable
fileSize = os.path.getsize(fileName)

# create output CSV with headers
nssHeaders = ['Time','Left Bay Door #1 Partial Open','Left Bay Door #1 Full Open','Left Bay Door #1 Closed','Left Bay Door #1 In Motion',
              'Right Bay Door #1 Partial Open','Right Bay Door #1 Full Open','Right Bay Door #1 Closed','Right Bay Door #1 In Motion',
              'Pilot Unlock Consent','WSO Unlock Consent', 'Left DR Not in CMD Position','Right DR Not in CMD Position','Control Lockout']
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
                # ***** Bay Lnchr Message *******************************************************************************************
                if (msg.data[0] == 5 and msg.data[1] == 118) or (msg.data[0] == 5 and msg.data[1] == 126):
                    LtRt_Bay_Door_Stat = msg.data[5]
                    LtRt_Bay_Door_Stat = (LtRt_Bay_Door_Stat << 8) + msg.data[4]
                    
                    L_Dr_Partial_Open = (LtRt_Bay_Door_Stat>>15)
                    L_Dr_Full_Open = (LtRt_Bay_Door_Stat>>14) & 0x1
                    L_Dr_Closed = (LtRt_Bay_Door_Stat>>13) & 0x1
                    L_Dr_In_Motion = (LtRt_Bay_Door_Stat>>12) & 0x1
                    R_Dr_Partial_Open = (LtRt_Bay_Door_Stat>>11)  & 0x1
                    R_Dr_Full_Open = (LtRt_Bay_Door_Stat>>10) & 0x1
                    R_Dr_Closed = (LtRt_Bay_Door_Stat>>9) & 0x1
                    R_Dr_In_Motion = (LtRt_Bay_Door_Stat>>8) & 0x1
                    Pilot_Unlock_Consent = (LtRt_Bay_Door_Stat>>7) & 0x1
                    WSO_Unlock_Consent = (LtRt_Bay_Door_Stat>>6) & 0x1
                    L_Dr_Not_In_CMD_Pos = (LtRt_Bay_Door_Stat>>5) & 0x1
                    R_Dr_Not_In_CMD_Pos = (LtRt_Bay_Door_Stat>>4) & 0x1
                    Control_Lockout = LtRt_Bay_Door_Stat & 0x1
                    
                    csvRow = [msg.get_time(),L_Dr_Partial_Open,L_Dr_Full_Open,L_Dr_Closed,L_Dr_In_Motion,R_Dr_Partial_Open,
                        R_Dr_Full_Open,R_Dr_Closed,R_Dr_In_Motion,Pilot_Unlock_Consent,WSO_Unlock_Consent,L_Dr_Not_In_CMD_Pos,
                        R_Dr_Not_In_CMD_Pos,Control_Lockout]
                    with open(outputFile,'a',newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(csvRow)
                # ***** End Bay Lnchr Message ***************************************************************************************
                    
        