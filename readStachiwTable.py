## Read Stachiw's table, and plot nominal annealing curves according to the input thickness
## Author: Jie Hu (jhu9@ualberta.ca)
###### prerequisite #####
## python version >= 3.10
## for ubuntu: sudo apt-get install libjpeg-dev zlib1g-dev
## pip install numpy
## pip install pandas
## pip install openpyxl
## pip install scipy
## pip install matplotlib
## pip install xlrd
## Disclaimer: The values from this code should be carefully considered by the users.
## The author is not responsible for any damage caused by the actual operations.
# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from numpy import *
from datetime import datetime
import matplotlib.pyplot as plt
import statistics as stat
from processCycle1and2 import handle_cycleMode_1_2
from processCycle3 import handle_cycleMode_3

# Display the dataframe
# print(df)
def main():
    print("*************************************")
    print("Set mode (conservative or fast)") 
    print("------- choose the mode carefully -------")
    print("press \'enter\': conservative mode (by default)") 
    print("press \'f\': fast (energy-save) mode")
    choice_mode = input("press:")
    run_mode = 0 # conservative mode by default
    if choice_mode == 'f':
       print("Set to fast mode. Warning: use the rate close to the maximum rate, be careful.")
       run_mode = 1
    elif choice_mode =="":
       print("Use conservative mode (by default)")
       run_mode = 0
    else:
       print("Use conservative mode (by default)")
       run_mode = 0
    
    print("*************************************")
    print(u"Set the room/ambient temperature (27 \N{DEGREE SIGN}C as default):")
    print("------- choose the season -------")
    print(u"press \'enter\': default (27\N{DEGREE SIGN}C)")
    print(u"press \'a\': spring/autumn (20\N{DEGREE SIGN}C)")
    print(u"press \'b\': summer (30\N{DEGREE SIGN}C)")
    print(u"press \'c\': winter (5\N{DEGREE SIGN}C)")
    print(u"or enter a temperature value: (in \N{DEGREE SIGN}C)")
    choice_temp = input("press/enter:")
    room_temp = 27 ## default value
    if choice_temp == 'a':
       room_temp = 20
       print(u"room temperature is set to 20\N{DEGREE SIGN}C for spring/autumn")
    elif choice_temp == 'b':
       room_temp = 30
       print(u"room temperature is set to 30\N{DEGREE SIGN}C for summer")
    elif choice_temp == 'c':
       room_temp = 5
       print(u"room temperature is set to 5\N{DEGREE SIGN}C for winter")
    elif choice_temp =="":
       print(u"room temperature is set to 27\N{DEGREE SIGN}C by default")  
    else:
       room_temp = ceil( int(choice_temp) )
       if room_temp>70 or room_temp<-70:
           print("Can you survive this room temperature?\nPlease enter again, range from -70 to 70 degC")
           while room_temp>70 or room_temp<-70:
               choice_temp = input("Enter:")
               room_temp = ceil( int(choice_temp) )
       print("room temperature is set to", room_temp, u"\N{DEGREE SIGN}C.")
    
    print("*************************************")
    print(u"Set the annealing cycle")
    print("------- choose the cycle -------")
    print("press 1: cycle 1 (table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, single-layer before machining)")
    print("press 2: cycle 2 (still table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, laminated layers")
    print("press 3: cycle 3 (table 15.3B), laminated-layer after machining)") 
    
    cycle_choice = input("press:")
    cycle_mode = int(cycle_choice)
    
    print("!!! Now we are checking with the annealing cycle "+str(cycle_mode))
    set_thickness = input("Enter acrylic thickness in mm:")
    while set_thickness=="":
        print("You must set the thickness value.")
        set_thickness = input("Enter acrylic thickness in mm:")
    
    thickness = float(set_thickness)    
    if thickness<0.0 or thickness>1000000.0:
       print("Wrong thickness value, try again. Range from 0 to 1000 meter.")
       while thickness>1000000.0 or thickness<0.0:
           set_thickness = input("Enter acrylic thickness in mm:")
           thickness = float(set_thickness) 
    
    print("thickness is set to", thickness, "mm.")
    
    inputdata = [run_mode, thickness, room_temp, cycle_mode]
    if cycle_mode != 3: 
        handle_cycleMode_1_2(inputdata)
    if cycle_mode == 3:
        handle_cycleMode_3(inputdata)

if __name__ == "__main__":
    main()
