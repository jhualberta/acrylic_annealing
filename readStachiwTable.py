## Read Stachiw's table, and plot nominal annealing curves according to the input thickness
## Author: Jie Hu (jhu9@ualberta.ca)
###### prerequisite #####
## python version >= 3.1
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

inch_to_mm = 25.4 # mm/inch

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32.)*5./9

### NOTE: for the temperature change, don't need to subtract 32*5./9 !!
def fahrenheit_to_celsius_rate(fahrenheit):
    return (fahrenheit)*5./9

def celsius_to_fahrenheit_rate(celsius):
    return (celsius)*9./5

##NOTE: turn on this tag, we will always use the thicker data value than we input
is_conservative = True
def find_closest_index( input_value, list_vals ):
    # Convert the list to a numpy array
    array_vals = np.array(list_vals)
    # Find the index of the closest value
    idx = (np.abs(array_vals - input_value)).argmin()
    #NOTE: we use a conservative curve:
    # if the thickness is slightly larger than the data by 1mm, we use the next larger data
    # if you don't want to be so conservative, set the is_conservative False
    if is_conservative:
        if (input_value - array_vals[idx]>1):
            idx = idx + 1
    return idx

current_dir = os.getcwd()
file_name_15_1 = 'StachiwTable15_1.csv'
#file_name_15_3 = 'StachiwTable15_3.csv'

file_path = os.path.join(current_dir, file_name_15_1)

#file_name = 'StachiwTable.csv'
#file_path = os.path.join(current_dir, file_name)
#
#file_name = 'StachiwTable.csv'
#file_path = os.path.join(current_dir, file_name)

# Read the Excel file, skipping the first 3 rows
df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')

#df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')
#df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')
#df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')

# Display the dataframe
# print(df)

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
       print("Can you survive this room temperature? Please enter again, range from -70 to 70 degC")
       while room_temp>70 or room_temp<-70:
           choice_temp = input("Enter:")
           room_temp = ceil( int(choice_temp) )
   print("room temperature is set to", room_temp, u"\N{DEGREE SIGN}C.")

print("*************************************")
print(u"Set the annealing cycle")
print("------- choose the cycle -------")
print("press 1: cycle 1 (table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, single-layer before machining)")
print("press 2: cycle 2 (same table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, laminated layers")
print("press 3: cycle 3 (table 15.3), laminated-layer after machining)") 

cycle_choice = input("press:")
cycleMode = int(cycle_choice)
print("!!! Now we are checking with the annealing cycle "+str(cycleMode))
thickness = float(input("Enter acrylic thickness in mm: "))
list_thickness = df.iloc[:, 1].tolist()
list_max_heatingRate = df.iloc[:, 2].tolist()
list_min_risetime_to140degC = df.iloc[:, 3].tolist()
list_holdTime_at140degC = df.iloc[:, 4].tolist() 
list_coolingRate_to110degC = df.iloc[:, 5].tolist()
list_decreasetime_to110degC = df.iloc[:, 6].tolist()
list_holdTime_at110degC = df.iloc[:, 7].tolist()
list_max_coolingRate_to27degC = df.iloc[:, 8].tolist()
list_decreasetime_to27degC = df.iloc[:, 9].tolist()
list_totaltime = df.iloc[:, 10].tolist() 

n_data = len(list_thickness)

row_index = 0

if thickness<=list_thickness[0]:
    print(str(thickness)+"mm is less than the minimum "+str(list_thickness[0])+"mm in Stachiw's database.")
    print("Use the "+str(list_thickness[0])+"mm curve [definitely safe].")
    row_index = 0
elif thickness>=list_thickness[-1]:
    print(str(thickness)+"mm is more than the maximum "+str(list_thickness[-1])+"mm in Stachiw's database.")
    print("Use the "+str(list_thickness[-1])+"mm curve [could be unsafe].")
    row_index = n_data - 1 
else:
    ## use the closest values in the row
    row_index = find_closest_index(thickness, list_thickness)

if is_conservative:
    print("Note: we are using conservative curve (a thicker acrylic curve in data than input).")

print("Extract the curve for "+ str( round(list_thickness[row_index],1) ) + "mm") 

max_heatingRate = list_max_heatingRate[row_index] 
max_heatingRate_degC = abs(fahrenheit_to_celsius_rate(max_heatingRate))
max_heatingRate_degC_minutes = max_heatingRate_degC/60

suggest_heatingRate_degC = floor(max_heatingRate_degC/10)*10

#NOTE: our fast mode value is already lower than the maximum value
fast_heatingRate_degC = floor(max_heatingRate_degC/2)*2

heatingRate_degC = suggest_heatingRate_degC
if run_mode == 1:#use fast mode
    heatingRate_degC = fast_heatingRate_degC

min_risetime_to140degC   = list_min_risetime_to140degC[row_index]
actual_risetime_to140degC = (140. - room_temp)/heatingRate_degC

holdTime_at140degC       = list_holdTime_at140degC[row_index]      
coolingRate_to230F       = list_coolingRate_to110degC[row_index]
coolingRate_to110degC    = fahrenheit_to_celsius_rate(coolingRate_to230F) 
decreasetime_to110degC   = list_decreasetime_to110degC[row_index]
holdTime_at110degC       = list_holdTime_at110degC[row_index]      
max_coolingRate_to80F    = list_max_coolingRate_to27degC[row_index]
max_coolingRate_to27degC = fahrenheit_to_celsius_rate(max_coolingRate_to80F)
decreasetime_to27degC    = list_decreasetime_to27degC[row_index]
totaltime                = list_totaltime[row_index]

max_heatingRate_degC     = round(max_heatingRate_degC,3)
coolingRate_to110degC    = round(coolingRate_to110degC,3)
max_coolingRate_to27degC = round(max_coolingRate_to27degC,3)
print("!!!!! max_heatingRate_degC", max_heatingRate_degC, "suggested", suggest_heatingRate_degC)
#print( 140. - room_temp, heatingRate_degC, actual_risetime_to140degC)
print("cooling-to-110degC:", coolingRate_to110degC)
print("cooling-to-roomTemp:", max_coolingRate_to27degC)

print(u"Note: the Stachiw's tables assume a default room temperature 27\N{DEGREE SIGN}C; here we use "+ str(room_temp) + "\N{DEGREE SIGN}C.")
print("----------------------------------------------------------------")
print(u"Max oven heating rate to 140\N{DEGREE SIGN}C (value in table):")
print( str(round(max_heatingRate_degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(max_heatingRate_degC_minutes,2)) + u"\N{DEGREE SIGN}C/minute" 
+ " or "+str(round(max_heatingRate,2)) + u"\N{DEGREE SIGN}F/hour")
if run_mode == 1:
    print(u"Fast (energy-save) oven heating rate to 140\N{DEGREE SIGN}C:")
else:
    print(u"Suggested conservative oven heating rate to 140\N{DEGREE SIGN}C:")
print( str(round(heatingRate_degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(heatingRate_degC/60,2)) + u"\N{DEGREE SIGN}C/minute or "
+ str(round( celsius_to_fahrenheit_rate(heatingRate_degC), 2)) + u"\N{DEGREE SIGN}F/hour" )

print("----------------------------------")
print(u"Time for heating to 140 \N{DEGREE SIGN}C (value in table):")
#print (round(min_risetime_to140degC,2), round(min_risetime_to140degC*60,2))
print( str(round(min_risetime_to140degC,2)) + " hours; or " + str(round(min_risetime_to140degC*60,2)) + " minutes")

if run_mode == 1:
    print(u"Fast/energy save time for heating to 140\N{DEGREE SIGN}C:")
else:
    print(u"Suggested/conservative time for heating to 140\N{DEGREE SIGN}C:")
print(str(round(actual_risetime_to140degC,2)) + " hours; or " + str(round(actual_risetime_to140degC*60,2)) + " minutes")

actual_totaltime = (140. - room_temp)/suggest_heatingRate_degC + holdTime_at140degC + (140. - 110.)/coolingRate_to110degC + holdTime_at110degC + (110. - room_temp)/max_coolingRate_to27degC

print("------------------------------------------------------")
print(u"Hold time at 140 \N{DEGREE SIGN}C:")
print( str(round(holdTime_at140degC,2)) + " hours; or "+ str(round(holdTime_at140degC*60,2)) + " minutes")
print("------------------------------------------------------")
print(u"Approx. cooling rate to 110 \N{DEGREE SIGN}C:")
print( str(round(coolingRate_to110degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(coolingRate_to110degC/60,2)) + u"\N{DEGREE SIGN}C/minute")
print( "or "+str(round(coolingRate_to230F,2)) + u"\N{DEGREE SIGN}F/hour")
print("------------------------------------------------------")
print(u"Hours to Cool oven to 110 \N{DEGREE SIGN}C:")
print( str( round(decreasetime_to110degC,2))+ " hours; or "+ str(round(decreasetime_to110degC*60,2)) + " minutes")
print("------------------------------------------------------")
print(u"Hold time at 110 \N{DEGREE SIGN}C:")
print( str(round(holdTime_at110degC,2)) + " hours")
print("------------------------------------------------------")
print(u"Max cooling rate to room temperature:")
print( str(round(max_coolingRate_to27degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(max_coolingRate_to27degC/60,2)) + u"\N{DEGREE SIGN}C/minute") 
print( "or "+str(round(max_coolingRate_to80F,2)) + u"\N{DEGREE SIGN}F/hour")
print("------------------------------------------------------")
print("Total time expected in Stachiw's table:")
print(str(totaltime) + " hours; or " + str( round(totaltime*60, 2) )+ " minutes")
print("Total time suggested:")
print(str(round(actual_totaltime,1)) + " hours; or " + str( np.ceil(actual_totaltime*60) )+ " minutes")
actual_days = actual_totaltime/24
if actual_totaltime>48:
    print("or " + str( int(actual_days) ) + " days and " + str( round(actual_totaltime - int(actual_days)*24, 1) ) + " hours.")
print("------------------------------------------------------")
## print the footnotes
df_note = pd.read_csv(file_path, skiprows=2)
footnotes = df_note.tail(3).iloc[:, 0]
note_texts = '\n'.join(footnotes.astype(str).tolist())
print(note_texts)

print("================ Making the plots now ================")
def stachiwCycle1(t):
    timeRegion1 = (140. - room_temp)/suggest_heatingRate_degC #max_heatingRate_degC
    timeRegion2 = timeRegion1 + holdTime_at140degC
    timeRegion3 = timeRegion2 + (140. - 110.)/coolingRate_to110degC
    timeRegion4 = timeRegion3 + holdTime_at110degC
    timeRegion5 = timeRegion4 + (110. - room_temp)/max_coolingRate_to27degC
    #print(max_heatingRate_degC, coolingRate_to110degC, max_coolingRate_to27degC)
    if 0 <= t<= timeRegion1:
        return suggest_heatingRate_degC*t + room_temp
    elif timeRegion1 < t <= timeRegion2:
        return 140
    elif timeRegion2 < t <= timeRegion3:
        return 140 - coolingRate_to110degC*(t-timeRegion2)
    elif timeRegion3 < t <= timeRegion4:
        return 110
    elif timeRegion4 <= t < timeRegion5:
        return 110 - max_coolingRate_to27degC*(t-timeRegion4)
    else:
        return None

### Stachiw bonded annealing
def stachiwCycle2(t):
    if 0 <= t<= 10:
        return 12*t + 20 ## 12C/hour
    elif 10 < t <= 60:
        return 140
    elif 60 < t <= 85:
        return 140 - 1.2*(t-60)
    elif 85 < t <= 110:
        return 110
    elif 110 <= t < 160:
        return 110 - 1.8*(t-110)
    else:
        return None

### Stachiw machined annealing
def stachiwCycle3(t):
    if 0 <= t<= 10:
        return 6.5*t + 20
    elif 10 < t <= 81:
        return 85
    elif 81 < t <= 113:
        return 85 - 2.0 * (t-81)
    else:
        return None

endTime = int(actual_totaltime) + 10 # for plotting 
plotTimeStep  = endTime*100
time_stachiwCycle1 = np.linspace(0, endTime, plotTimeStep)
time_stachiwCycle2 = np.linspace(0, endTime, plotTimeStep)
time_stachiwCycle3 = np.linspace(0, endTime, plotTimeStep)

temperature_stachiwCycle1 = [stachiwCycle1(t) for t in time_stachiwCycle1]
temperature_stachiwCycle2 = [stachiwCycle2(t) for t in time_stachiwCycle2]
temperature_stachiwCycle3 = [stachiwCycle3(t) for t in time_stachiwCycle3]

plt.plot(time_stachiwCycle1, temperature_stachiwCycle1,linestyle='dashed', label="Annealing cycle 1, raw single-layer")
plt.xlabel("hours")
plt.ylabel(u"Temperature (\N{DEGREE SIGN}C) ")
plt.grid(True, axis='x')
plt.grid(True, axis='y')
plt.legend()
####plt.xticks(rotation=45)
#plt.tight_layout()
savePlotName = "annealingCyle" + cycle_choice + "_" + str(thickness).replace('.','p') + "mm_" + str(room_temp).replace('.','p') +"degC.jpg"
# Save the plot to a JPG file
#NOTE: change the plot resolution as needed
#plt.savefig(savePlotName, format='jpg', dpi=200)  # dpi sets the resolution
plt.show()
plt.close()  # Close the plot to free up memory

## print the curve
print("insert the python codes below for plotting this curve:")
print("======================================================")
print("def stachiwCycle1(t):")
print("    room_temp = %.f"%room_temp)
print("    timeRegion1 = (140. - room_temp)/%.f"%heatingRate_degC)
print("    timeRegion2 = timeRegion1 + %.f ## hold for %.f hours at 140degC"%(holdTime_at140degC,holdTime_at140degC))
print("    timeRegion3 = timeRegion2 + (140. - 110.)/abs(%.2f)"%coolingRate_to110degC)
print("    timeRegion4 = timeRegion3 + %.f ## hold for %.f hours at 110degC"%(holdTime_at110degC,holdTime_at110degC))
print("    timeRegion5 = timeRegion4 + (110. - room_temp)/abs(%.2f)"%max_coolingRate_to27degC)
print("")
print("    if 0 <= t<= timeRegion1:")
print("        return %.2f*t + room_temp"%max_heatingRate_degC)
print("    elif timeRegion1 < t <= timeRegion2:")
print("        return 140")
print("    elif timeRegion2 < t <= timeRegion3:")
print("        return 140 + %.2f*(t-timeRegion2)"%coolingRate_to110degC)
print("    elif timeRegion3 < t <= timeRegion4:")
print("        return 110")
print("    elif timeRegion4 <= t < timeRegion5:")
print("        return 110 + %.2f*(t-timeRegion4)"%max_coolingRate_to27degC)
print("    else:")
print("        return None")
print("")
print("endTime = int(actual_totaltime) + 10 # for plotting")
print("plotTimeStep  = endTime*100")
print("time_stachiwCycle1 = np.linspace(0, endTime, plotTimeStep)")
print("time_stachiwCycle2 = np.linspace(0, endTime, plotTimeStep)")
print("time_stachiwCycle3 = np.linspace(0, endTime, plotTimeStep)")
print("temperature_stachiwCycle1 = [stachiwCycle1(t) for t in time_stachiwCycle1]")
print("temperature_stachiwCycle2 = [stachiwCycle2(t) for t in time_stachiwCycle2]")
print("temperature_stachiwCycle3 = [stachiwCycle3(t) for t in time_stachiwCycle3]")
print("")
print("plt.plot(time_stachiwCycle1, temperature_stachiwCycle1,linestyle=\'dashed\', label=\"Annealing cycle 1, raw single-layeri\")")
print("plt.xlabel(\"hours\")")
print("plt.ylabel(u\"Temperature (\N{DEGREE SIGN}C) \")")
print("plt.grid(True, axis=\'x\')")
print("plt.grid(True, axis=\'y\')")
print("plt.legend()")
print("plt.show()")
print("")

print("======================================================")
print("insert the root C++ codes below for plotting this curve:")
print("======================================================")
print("run the code by: root plotStachiwCycle.C")
# File name
filename_ROOTcode = "plotStachiwCycle.C"
rootCode_strings = [ 
"#include <iostream>",
"#include <vector>",
"#include <cmath>",
"#include \"TCanvas.h\"",
"#include \"TGraph.h\"",
"#include \"TAxis.h\"",
"#include \"TLegend.h\"",
"",
"// Function to represent stachiwCycle",
"double stachiwCycle1(double t) {",
"    double room_temp = "+ str(room_temp) + ";",
"    double timeRegion1 = (140.0 - room_temp)/" + str(heatingRate_degC) + ";",
"    double timeRegion2 = timeRegion1 + " + str(holdTime_at140degC) + ";  // Hold for " + str(holdTime_at140degC) + " hours at 140degC",
"    double timeRegion3 = timeRegion2 + (140.0 - 110.0)/std::abs(" + str(coolingRate_to110degC) + ");",
"    double timeRegion4 = timeRegion3 + " + str(holdTime_at110degC) +  ";   // Hold for " + str(holdTime_at110degC) + " hours at 110degC",
"    double timeRegion5 = timeRegion4 + (110.0 - room_temp)/std::abs(" + str(max_coolingRate_to27degC) + ");",
"",
"    if (0 <= t && t <= timeRegion1) {",
"        return " + str(heatingRate_degC) + "* t + room_temp;",
"    } else if (timeRegion1 < t && t <= timeRegion2) {",
"        return 140.0;",
"    } else if (timeRegion2 < t && t <= timeRegion3) {",
"        return 140.0 + -1*" + str(coolingRate_to110degC) + "*(t - timeRegion2);",
"    } else if (timeRegion3 < t && t <= timeRegion4) {",
"        return 110.0;",
"    } else if (timeRegion4 <= t && t < timeRegion5) {",
"        return 110.0 + -1*" + str(max_coolingRate_to27degC) + "*(t - timeRegion4);",
"    } else {",
"        return 0;  // Return 0 if t is out of bounds",
"    }",
"}",
"",
"void plotStachiwCycle() {",
"    // Time vectors for the different cycles",
"    int endTime = " + str( int(actual_totaltime) ) + "; // total time", 
"    int nPoints = endTime*100;",
"    std::vector<double> time_stachiwCycle1(nPoints);",
"    std::vector<double> temperature_stachiwCycle1(nPoints);",
"    ",
"    for (int i = 0; i < nPoints; ++i) {",
"        time_stachiwCycle1[i] = i*0.01;  // Fill the time values",
"        temperature_stachiwCycle1[i] = stachiwCycle1(time_stachiwCycle1[i]);",
"    }",
"",
"    // Create canvas",
"    TCanvas *c1 = new TCanvas(\"c1\", \"Annealing Cycle\", 800, 600);",
"",
"    // Create a graph",
"    TGraph *gr1 = new TGraph(nPoints, &time_stachiwCycle1[0], &temperature_stachiwCycle1[0]);",
"    gr1->SetLineColor(kGray+1);// Line color",
"    gr1->SetLineWidth(2);  // Line width",
"    gr1->SetLineStyle(2);  // Dashed line",
"    gr1->SetTitle(\"Annealing Cycle, raw single-layer\");",
"    gr1->GetXaxis()->SetTitle(\"Hours\");",
"    gr1->GetYaxis()->SetTitle(\"Temperature (^{#circ}C,\");",
"",
"    // Draw graph",
"    gr1->Draw(\"AL\");  // \"A\" for axes, \"L\" for line",
"",
"    // Grid and legend",
"    c1->SetGridx();",
"    c1->SetGridy();",
"    TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);",
"    legend->AddEntry(gr1, \"Annealing cycle 1, raw single-layer\", \"l\");",
"    legend->Draw();",
"",
"    // Show plot",
"    c1->Update();",
"    c1->Draw();",
"}"]

# Write strings to the .C file
with open(filename_ROOTcode, "w") as file:
    for line in rootCode_strings:
        file.write(line + "\n")
print(f"File '{filename_ROOTcode}' has been created.")

#print("======================================================")
