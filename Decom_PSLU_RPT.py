
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
outputFile = fileName[:-4] + "_PSLU_RPT.csv"
# progress bar variable
fileSize = os.path.getsize(fileName)

# create output CSV with headers
nssHeaders = ['Time','LM DR CLLK S','LM DR OPEN S','RM DR CLLK S','RM DR OPEN S']
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
                # ***** PSLU Message *******************************************************************************************
                if msg.data[0] == 14 and msg.data[1] == 35:
                    LR_MlgDr_Pos_S = msg.data[5]
                    LR_MlgDr_Pos_S = (LR_MlgDr_Pos_S << 8) + msg.data[4]
                    
                    Lm_Dr_Cllk_S = (LR_MlgDr_Pos_S>>15)
                    Lm_Dr_Open_S = (LR_MlgDr_Pos_S>>14) & 0x1
                    Rm_Dr_Cllk_S = (LR_MlgDr_Pos_S>>9) & 0x1
                    Rm_Dr_Open_S = (LR_MlgDr_Pos_S>>8) & 0x1
                    
                    csvRow = [msg.get_time(),Lm_Dr_Cllk_S,Lm_Dr_Open_S,Rm_Dr_Cllk_S,Rm_Dr_Open_S]
                    with open(outputFile,'a',newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(csvRow)
                # ***** End PSLU Message ***************************************************************************************
                    
        