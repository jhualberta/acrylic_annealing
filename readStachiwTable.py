## Read Stachiw's table, and plot nominal annealing curves according to the input thickness
## Author: Jie Hu (jhu9@ualberta.ca)
###### prerequisite #####
## > python 3.1
## for ubuntu: sudo apt-get install libjpeg-dev zlib1g-dev
## pip install numpy
## pip install pandas
## pip install openpyxl
## pip install scipy
## pip install matplotlib
## pip install xlrd
import os
import pandas as pd
import numpy as np
from numpy import *
from datetime import datetime
import matplotlib.pyplot as plt
import statistics as stat

inch_to_mm = 25.4 # mm/inch
##NOTE: turn on this tag, we will always use the thicker data value than we input
is_conservative = True

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32.)*5./9

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
file_name = 'StachiwTable.csv'
file_path = os.path.join(current_dir, file_name)

# Read the Excel file, skipping the first 3 rows
df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')

# Display the dataframe
# print(df)
print(u"Set the room/ambient temperature (27 \N{DEGREE SIGN}C as default):")
print("------- choose the season -------")
print(u"press 1 for spring/autumn (20\N{DEGREE SIGN}C)")
print(u"press 2 for summer (30\N{DEGREE SIGN}C)")
print(u"press 3 for winter (5\N{DEGREE SIGN}C)")
print(u"press enter as default (27\N{DEGREE SIGN}C)")
choice = input("press:")
room_temp = 27
if choice == 1:
   room_temp = 20
elif choice == 2:
   room_temp = 30
elif choice == 3:
   room_temp = 5
elif choice =="":
   print(u"room temperature is set to 27\N{DEGREE SIGN}C by default")  
else:
   print(u"room temperature is set to 27\N{DEGREE SIGN}C by default")

thickness = float(input("Enter acrylic thickness in mm: "))
list_thickness = df.iloc[:, 1].tolist()
list_max_heatingRate = df.iloc[:, 2].tolist()
list_risetime_to140degC = df.iloc[:, 3].tolist()
list_holdtime_at140degC = df.iloc[:, 4].tolist() 
list_coolingRate_to110degC = df.iloc[:, 5].tolist()
list_decreasetime_to110degC = df.iloc[:, 6].tolist()
list_holdtime_at110degC = df.iloc[:, 7].tolist()
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
max_heatingRate_degC = abs(fahrenheit_to_celsius(max_heatingRate))
max_heatingRate_degC_minutes = max_heatingRate_degC/60

risetime_to140degC       = list_risetime_to140degC[row_index]
holdtime_at140degC       = list_holdtime_at140degC[row_index]      
coolingRate_to230F       = list_coolingRate_to110degC[row_index]
coolingRate_to110degC    = fahrenheit_to_celsius(coolingRate_to230F) 
decreasetime_to110degC   = list_decreasetime_to110degC[row_index]
holdtime_at110degC       = list_holdtime_at110degC[row_index]      
max_coolingRate_to80F    = list_max_coolingRate_to27degC[row_index]
max_coolingRate_to27degC = fahrenheit_to_celsius(max_coolingRate_to80F)
decreasetime_to27degC    = list_decreasetime_to27degC[row_index]
totaltime                = list_totaltime[row_index]
print(u"Note: the numbers below are for room temperature 27\N{DEGREE SIGN}C")
print("----------------------------------")
print(u"Max oven heating rate to 140\N{DEGREE SIGN}C:")
print( str(round(max_heatingRate_degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(max_heatingRate_degC_minutes,2)) + u"\N{DEGREE SIGN}C/minute")
print( "or "+str(round(max_heatingRate,2)) + u"\N{DEGREE SIGN}F/hour")
print("----------------------------------")
print(u"Time for heating to 140 \N{DEGREE SIGN}C:")
print( str(round(risetime_to140degC,2)) + " hours; or " + str(round(risetime_to140degC*60,2)) + " minutes")
print("----------------------------------")
print(u"Hold time at 140 \N{DEGREE SIGN}C:")
print( str(round(holdtime_at140degC,2)) + " hours; or "+ str(round(holdtime_at140degC*60,2)) + " minutes")
print("----------------------------------")
print(u"Approx. cooling rate to 110 \N{DEGREE SIGN}C:")
print( str(round(coolingRate_to110degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(coolingRate_to110degC/60,2)) + u"\N{DEGREE SIGN}C/minute")
print( "or "+str(round(coolingRate_to230F,2)) + u"\N{DEGREE SIGN}F/hour")
print("----------------------------------")
print(u"Hours to Cool oven to 110 \N{DEGREE SIGN}C:")
print( str( round(decreasetime_to110degC,2))+ " hours; or "+ str(round(decreasetime_to110degC*60,2)) + " minutes")
print("----------------------------------")
print(u"Hold time at 110 \N{DEGREE SIGN}C:")
print( str(round(holdtime_at110degC,2)) + " hours")
print("----------------------------------")
print(u"Max cooling rate to room temperature:")
print( str(round(max_coolingRate_to27degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(max_coolingRate_to27degC/60,2)) + u"\N{DEGREE SIGN}C/minute") 
print( "or "+str(round(max_coolingRate_to80F,2)) + u"\N{DEGREE SIGN}F/hour")
print("----------------------------------")
print( "Total time expected:")
print( str(totaltime) + " hours; or " + str( round(totaltime*60, 2) )+ " minutes")
## print the footnotes
df_note = pd.read_csv(file_path, skiprows=2)
footnotes = df_note.tail(3).iloc[:, 0]
note_texts = '\n'.join(footnotes.astype(str).tolist())
print(note_texts)

print("================ Making the plots now ================")
print("======================================================")
def stachiwCycle1(t):
    timeRegion1 = (140. - room_temp)/max_heatingRate_degC #risetime_to140degC
    timeRegion2 = timeRegion1 + holdtime_at140degC
    timeRegion3 = timeRegion2 + (140. - 110.)/abs(coolingRate_to110degC)
    timeRegion4 = timeRegion3 + holdtime_at110degC
    timeRegion5 = timeRegion4 + (110. - room_temp)/abs(max_coolingRate_to27degC)
    #print(max_heatingRate_degC, coolingRate_to110degC, max_coolingRate_to27degC)
    if 0 <= t<= timeRegion1:
        return max_heatingRate_degC*t + room_temp
    elif timeRegion1 < t <= timeRegion2:
        return 140
    elif timeRegion2 < t <= timeRegion3:
        return 140 + coolingRate_to110degC*(t-timeRegion2)
    elif timeRegion3 < t <= timeRegion4:
        return 110
    elif timeRegion4 <= t < timeRegion5:
        return 110 + max_coolingRate_to27degC*(t-timeRegion4)
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


time_stachiwCycle1 = np.linspace(0, 400, 400)
time_stachiwCycle2 = np.linspace(0, 400, 400)
time_stachiwCycle3 = np.linspace(0, 400, 400)

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
plt.show()
## print the curve
print("insert the python codes below for plotting this curve:")
print("======================================================")
print("def stachiwCycle1(t):")
print("    room_temp = %.f"%room_temp)
print("    timeRegion1 = (140. - room_temp)/%.f"%max_heatingRate_degC)
print("    timeRegion2 = timeRegion1 + %.f ## hold for %.f hours at 140degC"%(holdtime_at140degC,holdtime_at140degC))
print("    timeRegion3 = timeRegion2 + (140. - 110.)/abs(%.2f)"%coolingRate_to110degC)
print("    timeRegion4 = timeRegion3 + %.f ## hold for %.f hours at 110degC"%(holdtime_at110degC,holdtime_at110degC))
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
print("time_stachiwCycle1 = np.linspace(0, 400, 400)")
print("time_stachiwCycle2 = np.linspace(0, 400, 400)")
print("time_stachiwCycle3 = np.linspace(0, 400, 400)")
print("temperature_stachiwCycle1 = [stachiwCycle1(t) for t in time_stachiwCycle1]")
print("temperature_stachiwCycle2 = [stachiwCycle2(t) for t in time_stachiwCycle2]")
print("temperature_stachiwCycle3 = [stachiwCycle3(t) for t in time_stachiwCycle3]")
print("plt.plot(time_stachiwCycle1, temperature_stachiwCycle1,linestyle='dashed', label=\"Annealing cycle 1, raw single-layer\") ")
print("plt.xlabel(\"hours\")")
print("plt.ylabel(u\"Temperature (\\N{DEGREE SIGN}C) \")")
print("plt.grid(True, axis=\'x\')")
print("plt.grid(True, axis=\'y\')")
print("plt.legend()")
print("plt.show()")
print("")
print("======================================================")
print("insert the root C++ codes below for plotting this curve:")
print("======================================================")
print("#include <iostream>")
print("#include <vector>")
print("#include <cmath>")
print("#include \"TCanvas.h\"")
print("#include \"TGraph.h\"")
print("#include \"TAxis.h\"")
print("#include \"TLegend.h\"")
print("")
print("// Function to represent stachiwCycle1")
print("double stachiwCycle1(double t) {")
print("    double room_temp = 27;")
print("    double timeRegion1 = (140.0 - room_temp) / 20.0;")
print("    double timeRegion2 = timeRegion1 + 14.0;  // Hold for 14 hours at 140°C")
print("    double timeRegion3 = timeRegion2 + (140.0 - 110.0) / std::abs(-13.33);")
print("    double timeRegion4 = timeRegion3 + 7.0;   // Hold for 7 hours at 110°C")
print("    double timeRegion5 = timeRegion4 + (110.0 - room_temp) / std::abs(-12.22);")
print("")
print("    if (0 <= t && t <= timeRegion1) {")
print("        return 20.0 * t + room_temp;")
print("    } else if (timeRegion1 < t && t <= timeRegion2) {")
print("        return 140.0;")
print("    } else if (timeRegion2 < t && t <= timeRegion3) {")
print("        return 140.0 + -13.33 * (t - timeRegion2);")
print("    } else if (timeRegion3 < t && t <= timeRegion4) {")
print("        return 110.0;")
print("    } else if (timeRegion4 <= t && t < timeRegion5) {")
print("        return 110.0 + -12.22 * (t - timeRegion4);")
print("    } else {")
print("        return NAN;  // Return NaN if t is out of bounds")
print("    }")
print("}")
print("")
print("void plotStachiwCycle1() {")
print("    // Time vectors for the different cycles")
print("    int nPoints = 400;")
print("    std::vector<double> time_stachiwCycle1(nPoints);")
print("    std::vector<double> temperature_stachiwCycle1(nPoints);")
print("    ")
print("    for (int i = 0; i < nPoints; ++i) {")
print("        time_stachiwCycle1[i] = i;  // Fill the time values")
print("        temperature_stachiwCycle1[i] = stachiwCycle1(time_stachiwCycle1[i]);")
print("    }")
print("")
print("    // Create canvas")
print("    TCanvas *c1 = new TCanvas(\"c1\", \"Annealing Cycle\", 800, 600);")
print("")
print("    // Create a graph")
print("    TGraph *gr1 = new TGraph(nPoints, &time_stachiwCycle1[0], &temperature_stachiwCycle1[0]);")
print("    gr1->SetLineStyle(2);  // Dashed line")
print("    gr1->SetTitle(\"Annealing Cycle 1, raw single-layer\");")
print("    gr1->GetXaxis()->SetTitle(\"Hours\");")
print("    gr1->GetYaxis()->SetTitle(\"Temperature (^{#circ}C)\");")
print("")
print("    // Draw graph")
print("    gr1->Draw(\"AL\");  // \"A\" for axes, \"L\" for line")
print("")
print("    // Grid and legend")
print("    c1->SetGridx();")
print("    c1->SetGridy();")
print("    TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);")
print("    legend->AddEntry(gr1, \"Annealing cycle 1, raw single-layer\", \"l\");")
print("    legend->Draw();")
print("")
#print("    // Show plot")
#print("    c1->Update();")
#print("    c1->Draw();")
print("}")
print("======================================================")
