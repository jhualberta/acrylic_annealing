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

def celsius_to_fahrenheit(celsius):
    return celsius*9./5 + 32.

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

def handle_cycleMode_3(inputdata):
    #print(inputdata)
    run_mode     = inputdata[0]
    thickness    = inputdata[1]
    room_temp    = inputdata[2]
    cycle_mode   = inputdata[3] 
    cycle_choice = str(cycle_mode) 

    current_dir     = os.getcwd()
    file_name_15_3B = 'StachiwTable15_3B.csv'
    
    file_path = os.path.join(current_dir, file_name_15_3B)
    # Read the Excel file 15.3B, skipping the first 3 rows
    df = pd.read_csv(file_path, skiprows=2, skipfooter=3,engine='python')

    ##NOTE: the cooling rate uses the rate in the Table 15.1 for cooling from 110 degC to room temperature
    file_name_15_1 = 'StachiwTable15_1.csv'
    file_path1 = os.path.join(current_dir, file_name_15_1)
    # Read the Excel file, skipping the first 3 rows
    df1 = pd.read_csv(file_path1, skiprows=2, skipfooter=3,engine='python')
    print("======================================================================================================")
    print("!!! Important: For cycle 3, we heat the sample to 185\N{DEGREE SIGN}F (85\N{DEGREE SIGN}C) as default.")
    print("This is a conservative procedure and set as default. Make sure to select the proper heating target.")
    print("See Stachiw Page 838 or README for details.")
    print("------- choose the heating target carefully -------")
    print("press enter: Heat to 185\N{DEGREE SIGN}F (85\N{DEGREE SIGN}C) (default)")
    print("press a: Heat to 230\N{DEGREE SIGN}F (110\N{DEGREE SIGN}C)")
    print("press b: Heat to 212\N{DEGREE SIGN}F (100\N{DEGREE SIGN}C)")
    print("press c: Heat to 195\N{DEGREE SIGN}F (90\N{DEGREE SIGN}C)")

    max_temp = 85 # conservative mode by default
    choice_heat = input("press:")
    if choice_heat == "":
       max_temp = 85
    elif choice_heat == 'a':
       max_temp = 110
    elif choice_heat == 'b':
       max_temp = 100
    elif choice_heat == 'c':
       max_temp = 90  
    else:
       print("Wrong input. Set to the default 85 degC.")
       max_temp = 85
    print("!!! Sample will be heated up to", max_temp, "\N{DEGREE SIGN}C.")

    max_temp_degF = celsius_to_fahrenheit(max_temp) 
    #Load table 15.3B
    list_thickness1       = df.iloc[:, 0].tolist() # thickness range1
    list_thickness2       = df.iloc[:, 1].tolist() # thickness range2
    list_max_heatingRate  = df.iloc[:, 2].tolist() # in fahrenheit
    
    list_holdTime_at110degC = df.iloc[:, 3].tolist() # in hour 
    list_holdTime_at100degC = df.iloc[:, 4].tolist() # in hour 
    list_holdTime_at90degC  = df.iloc[:, 5].tolist() # in hour 
    list_holdTime_at85degC  = df.iloc[:, 6].tolist() # in hour 
    n_data = len(list_thickness1)

    #Load table 15.1
    list_thickness_table1         = df1.iloc[:, 1].tolist()
    list_max_coolingRate_to27degC = df1.iloc[:, 8].tolist()
    list_decreasetime_to27degC    = df1.iloc[:, 9].tolist() 
    n_data1 = len(list_thickness_table1) # table 15.1
    
    row_index = 0 # search thickness range1
    row_index1 = 0 # search table 15.1
    if thickness<=list_thickness1[0]:
        print(str(thickness)+"mm is less than the minimum "+str(list_thickness1[0])+"mm in Stachiw's database.")
        print("Use the "+str(list_thickness1[0])+"mm curve [definitely safe].")
        row_index = 0
        row_index1 = 0
    elif thickness>=list_thickness2[-1]:
        print(str(thickness)+"mm is more than the maximum "+str(list_thickness2[-1])+"mm in Stachiw's database.")
        print("Use the "+str(list_thickness2[-1])+"mm curve [could be unsafe].")
        row_index  = n_data - 1
        row_index1 = n_data1 - 1 
    else:
        ## use the closest values in the row. 
        # For table 15.3B, thickness_range1< thickness < thiness_range2
        # the following procedure finds the row index1 of range1 and row index2 of range2; in most cases the values should be
        # same, while the row index2 could be one line above.
        row_index_range1 = find_closest_index(thickness, list_thickness1)
        row_index_range2 = find_closest_index(thickness, list_thickness2)
        thickness_range1 = list_thickness1[row_index_range1]
        thickness_range2 = list_thickness1[row_index_range2]
        row_index = row_index_range1
        if row_index_range2 < row_index_range1:
            if list_thickness1[row_index_range2]<thickness and thickness<list_thickness2[row_index_range2]:
                row_index = row_index_range2
        row_index1 = find_closest_index(thickness, list_thickness_table1)

    print("======================================================================================================")
    print("Extract the curve for the thickness in the range", round(list_thickness1[row_index],1), "to", round(list_thickness2[row_index],1),"mm (", round(list_thickness1[row_index]/25.4,1),"to", round(list_thickness2[row_index]/25.4,1), "inches).")
    max_heatingRate = list_max_heatingRate[row_index]
    max_heatingRate_degC = abs(fahrenheit_to_celsius_rate(max_heatingRate)) # degF/hr to degC/hr
    max_heatingRate_degC_minutes = max_heatingRate_degC/60
    suggest_heatingRate_degC = floor(max_heatingRate_degC)

    #NOTE: our fast mode value is already lower than the maximum value
    fast_heatingRate_degC = max_heatingRate_degC
    
    heatingRate_degC = suggest_heatingRate_degC
    if run_mode == 1:#use fast mode
        heatingRate_degC = fast_heatingRate_degC
    
    actual_risetime = (max_temp - room_temp)/heatingRate_degC

    holdTime = list_holdTime_at85degC[row_index]
    if max_temp == 90:
        holdTime = list_holdTime_at90degC[row_index]
    if max_temp == 100:
        holdTime = list_holdTime_at100degC[row_index]
    if max_temp == 100:
        holdTime = list_holdTime_at100degC[row_index]
   
    #search these values in 15.3B
    max_coolingRate_to27degC_fahren = list_max_coolingRate_to27degC[row_index1]
    max_coolingRate_to27degC = fahrenheit_to_celsius_rate(max_coolingRate_to27degC_fahren)
    decreasetime_to27degC    = list_decreasetime_to27degC[row_index1]
    max_coolingRate_to27degC = round(max_coolingRate_to27degC,3)
    print(u"Note: the Stachiw's tables always assume a default room temperature 27\N{DEGREE SIGN}C; here we use ", str(room_temp),"\N{DEGREE SIGN}C.")
    print("Be careful if the room temperature is very low.")
    print("The oven is supposed to heat up to ", max_temp, u"\N{DEGREE SIGN}C or ", round(max_temp_degF,1), "\N{DEGREE SIGN}F.")
    print("!!!!! Maximum heating rate is (value in Table 15.3B):")
    #print( 140. - room_temp, heatingRate_degC, actual_risetime)
    print("----------------------------------------------------------------")
    print(round(max_heatingRate_degC,2), u"\N{DEGREE SIGN}C/hour; or ", round(max_heatingRate_degC_minutes,2), u"\N{DEGREE SIGN}C/minute or", round(max_heatingRate,2), u"\N{DEGREE SIGN}F/hour")
    print("Warning: never faster than this rate!")
    if run_mode == 1:
        print(u"Fast (energy-save) oven heating rate to ", max_temp, "\N{DEGREE SIGN}C:")
    else:
        print(u"Suggested conservative oven heating rate to", max_temp, "\N{DEGREE SIGN}C:") 
    print(round(heatingRate_degC,2),u"\N{DEGREE SIGN}C/hour; or ", round(heatingRate_degC/60,2), u"\N{DEGREE SIGN}C/minute or", round( celsius_to_fahrenheit_rate(heatingRate_degC), 2), u"\N{DEGREE SIGN}F/hour" )
    
    print("----------------------------------")
    print(u"Time for heating to ", str(max_temp), "\N{DEGREE SIGN}C (value in table):")
    if run_mode == 1:
        print(u"Fast/energy save time for heating to " + str(max_temp) + "\N{DEGREE SIGN}C:")
    else:
        print(u"Suggested/conservative time for heating to " + str(max_temp) + "\N{DEGREE SIGN}C:")
    print(str(round(actual_risetime,2)) + " hours; or " + str(round(actual_risetime*60,2)) + " minutes.")
    
    actual_totaltime = (max_temp - room_temp)/suggest_heatingRate_degC + holdTime + (max_temp - room_temp)/max_coolingRate_to27degC
    totaltime = (max_temp - room_temp)/max_heatingRate_degC + holdTime + (max_temp - room_temp)/max_coolingRate_to27degC 
    print("------------------------------------------------------")
    print(u"Hold time at " + str (max_temp) + "\N{DEGREE SIGN}C:")
    print( str(round(holdTime,2)) + " hours; or "+ str(round(holdTime*60,2)) + " minutes.")
    print("------------------------------------------------------")
    print(u"Max cooling rate to room temperature:")
    print( str(round(max_coolingRate_to27degC,2)) + u"\N{DEGREE SIGN}C/hour; or " + str(round(max_coolingRate_to27degC/60,2)) + u"\N{DEGREE SIGN}C/minute or "+str(round(max_coolingRate_to27degC_fahren,2)) + u"\N{DEGREE SIGN}F/hour")
    cooling_time = (max_temp - room_temp)/max_coolingRate_to27degC
    print("Time for cooling to room temperature: " + str(round(cooling_time,2)) + " hours; or " + str(round(cooling_time*60,2)) + " minutes.")
    print("------------------------------------------------------")
    print("Total time expected in Stachiw's table:")
    print(str( round(totaltime,2) ) + " hours; or " + str( round(totaltime*60, 2) )+ " minutes.")
    print("Total time suggested:")
    print(str(round(actual_totaltime,1)) + " hours; or " + str( np.ceil(actual_totaltime*60) )+ " minutes.")
    actual_days = actual_totaltime/24
    if actual_totaltime>48:
        print("or " + str( int(actual_days) ) + " days and " + str( round(actual_totaltime - int(actual_days)*24, 1) ) + " hours.")
    print("------------------------------------------------------")
    print("After completion of the cycle, make sure the temperature must not")
    print("exceed the ambient room temperature by more than 8 \N{DEGREE SIGN}C;")
    print("i.e., must be below " + str(room_temp+8) + "\N{DEGREE SIGN}C.")
    print("------------------------------------------------------")
    ## print the footnotes
    #df_note = pd.read_csv(file_path, skiprows=2)
    #footnotes = df_note.tail(3).iloc[:, 0]
    #note_texts = '\n'.join(footnotes.astype(str).tolist())
    #print(note_texts)
    
    print("================ Making the plots now ================")
    def stachiwCycle3(t):
        timeRegion1 = (max_temp - room_temp)/suggest_heatingRate_degC #max_heatingRate_degC
        timeRegion2 = timeRegion1 + holdTime
        timeRegion3 = timeRegion2 + (max_temp - room_temp)/max_coolingRate_to27degC 

        if 0 <= t<= timeRegion1:
            return suggest_heatingRate_degC*t + room_temp 
        elif timeRegion1 < t <= timeRegion2: 
            return max_temp 
        elif timeRegion2 < t <= timeRegion3:
            return max_temp - max_coolingRate_to27degC*(t-timeRegion2) 
        else:
            return None
    
    endTime = int(actual_totaltime) + 10 # for plotting 
    plotTimeStep  = endTime*100
    time_stachiwCycle3 = np.linspace(0, endTime, plotTimeStep)
    
    temperature_stachiwCycle3 = [stachiwCycle3(t) for t in time_stachiwCycle3]
    
    plt.plot(time_stachiwCycle3, temperature_stachiwCycle3,linestyle='dashed', label="Annealing cycle 3, laminated panel after machining")
    plt.xlabel("hours")
    plt.ylabel(u"Temperature (\N{DEGREE SIGN}C) ")
    plt.grid(True, axis='x')
    plt.grid(True, axis='y')
    plt.legend()
    ####plt.xticks(rotation=45)
    #plt.tight_layout()
    savePlotName = "annealingCyle3" + "_" + str(thickness).replace('.','p') + "mm_" + str(room_temp).replace('.','p') +"degC.jpg"
    # Save the plot to a JPG file
    #NOTE: change the plot resolution as needed
    #plt.savefig(savePlotName, format='jpg', dpi=200)  # dpi sets the resolution
    plt.show()
    plt.close()  # Close the plot to free up memory
    
    ## print the curve
    print("insert the python codes below for plotting this curve:")
    print("======================================================")
    print("import numpy as np")
    print("from numpy import *")
    print("import matplotlib.pyplot as plt")
    print("room_temp = %.f"%room_temp)
    print("max_temp = %.f"%max_temp)
    print("holdTime =  %.f"%holdTime)
    print("suggest_heatingRate_degC = %.f"%suggest_heatingRate_degC) 
    print("max_coolingRate_to27degC = %.f"%max_coolingRate_to27degC)
    print("def stachiwCycle3(t):")
    print("    timeRegion1 = (max_temp - room_temp)/suggest_heatingRate_degC #max_heatingRate_degC")
    print("    timeRegion2 = timeRegion1 + holdTime")
    print("    timeRegion3 = timeRegion2 + (max_temp - room_temp)/max_coolingRate_to27degC")
    print("    if 0 <= t<= timeRegion1:")
    print("        return suggest_heatingRate_degC*t + room_temp")
    print("    elif timeRegion1 < t <= timeRegion2:")
    print("        return max_temp")
    print("    elif timeRegion2 < t <= timeRegion3:")
    print("        return max_temp - max_coolingRate_to27degC*(t-timeRegion2)")
    print("    else:")
    print("        return None")
    print("actual_totaltime = %.f"%actual_totaltime)
    print("endTime = int(actual_totaltime) + 10 # for plotting")
    print("plotTimeStep  = endTime*100")
    print("time_stachiwCycle3 = np.linspace(0, endTime, plotTimeStep)")
    print("temperature_stachiwCycle3 = [stachiwCycle3(t) for t in time_stachiwCycle3]")
    print("plt.plot(time_stachiwCycle3, temperature_stachiwCycle3,linestyle=\'dashed\', label=\"Annealing cycle 3, laminated panel after machining\")")
    print("plt.xlabel(\"hours\")")
    print("plt.ylabel(u\"Temperature (\\N{DEGREE SIGN}C)\")")
    print("plt.grid(True, axis=\'x\')")
    print("plt.grid(True, axis=\'y\')")
    print("plt.legend()")
    print("plt.show()")

    print("======================================================")
    print("save the root C++ codes below for plotting this curve:")
    print("======================================================")
    print("run the code by: root plotStachiwCycle3.C")
    # ROOT C++ file name
    filename_ROOTcode = "plotStachiwCycle3.C"
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
    "double room_temp = "+str(room_temp)+";",
    "double max_temp = "+str(max_temp)+";",
    "double holdTime = "+str(holdTime)+";",
    "double suggest_heatingRate_degC = "+str(suggest_heatingRate_degC)+";",
    "double max_coolingRate_to27degC = "+str(max_coolingRate_to27degC)+";",
    "double stachiwCycle3(double t) {",
    "    double timeRegion1 = (max_temp - room_temp)/suggest_heatingRate_degC;",
    "    double timeRegion2 = timeRegion1 + holdTime;  // Hold for " + str(holdTime) + " hours at " + str(max_temp)+ "degC",
    "    double timeRegion3 = timeRegion2 + (max_temp - room_temp)/max_coolingRate_to27degC;",
    "",
    "    if (0 <= t && t <= timeRegion1) {",
    "        return " + str(heatingRate_degC) + "* t + room_temp;",
    "    } else if (timeRegion1 < t && t <= timeRegion2) {",
    "        return max_temp;",
    "    } else if (timeRegion2 < t && t <= timeRegion3) {",
    "        return max_temp + -1*max_coolingRate_to27degC*(t - timeRegion2);",
    "    } else {",
    "        return 0;  // Return 0 if t is out of bounds",
    "    }",
    "}",
    "",
    "void plotStachiwCycle3() {",
    "    // Time vectors for the different cycles",
    "    int endTime = " + str( int(actual_totaltime) ) + "; // total time",
    "    int nPoints = endTime*100;",
    "    std::vector<double> time_stachiwCycle3(nPoints);",
    "    std::vector<double> temperature_stachiwCycle3(nPoints);",
    "    ",
    "    for (int i = 0; i < nPoints; ++i) {",
    "        time_stachiwCycle3[i] = i*0.01;  // Fill the time values",
    "        temperature_stachiwCycle3[i] = stachiwCycle3(time_stachiwCycle3[i]);",
    "    }",
    "",
    "    // Create canvas",
    "    TCanvas *c1 = new TCanvas(\"c1\", \"Annealing Cycle\", 800, 600);",
    "",
    "    // Create a graph",
    "    TGraph *gr1 = new TGraph(nPoints, &time_stachiwCycle3[0], &temperature_stachiwCycle3[0]);",
    "    gr1->SetLineColor(kGray+1);// Line color",
    "    gr1->SetLineWidth(2);  // Line width",
    "    gr1->SetLineStyle(3);  // Dashed line",
    "    gr1->SetTitle(\"Annealing Cycle 3, laminated panel after machining\");",
    "    gr1->GetXaxis()->SetTitle(\"Hours\");",
    "    gr1->GetYaxis()->SetTitle(\"Temperature (^{#circ}C),\");",
    "",
    "    // Draw graph",
    "    gr1->Draw(\"AL\");  // \"A\" for axes, \"L\" for line",
    "",
    "    // Grid and legend",
    "    c1->SetGridx();",
    "    c1->SetGridy();",
    "    TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);",
    "    legend->AddEntry(gr1, \"Annealing cycle3, laminated panel after machining\", \"l\");",
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

