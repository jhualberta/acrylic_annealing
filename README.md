# Introduction
This program suggests the annealing schedules for the casting acrylic based on
Chapter 15 Stress Relieving Processes,
Handbook of Acrylic, by Jerry D. Stachiw 
# Prerequisite
python version >= 3.6

install necessary packages:
```
pip install numpy
pip install pandas
pip install openpyxl
pip install scipy
pip install matplotlib
pip install xlrd
```
for ubuntu user:

`sudo apt-get install libjpeg-dev zlib1g-dev`

# Disclaimer: 
The values from this code should be carefully considered by the users.
The author is not responsible for any damage caused by the actual operations.

# Description
The excel file: allStachiwTablesCh15.xlsx with sheets contain three tables (15.1, 15.3 part A and 15.3 part B.) 
taken from Chapter 15 in Statichw's acrylic manual, for the topic of annealing the casting acrylic.
Table 15.2 is for the thermal shrinking, not yet included.
This file is saved here as a reference database, and a digitalized copy of the original tables from the book.
Two pdf files are scanned copies from the book.

The main program readStachiwTable.py, reads the CSV file `StachiwTable15_1.csv`
for the annealing cycle 1 and 2; and `StachiwTable15_3B.csv` for the annealing cycle 3.

Note for the annealing cycle 3, Stachiw suggests to heat up to 85°C or 185°F. There are other options but see the quotations below:

(Quoted from page 838) "As a rule, fabricators of acrylic components select 185°F temperature for surface annealing since in most cases the castings from which the items were made were not previously normalized or shrunk. Annealing such machined items at temperatures above 185°F might induce some undesirable dimensional changes due to presence of internal stresses that were not removed prior to machining by normalizing or shrinking thermal treatment. The drawback of using such a low annealing temperature is that the remaining residual stresses are probably somewhat higher than if the annealing was performed at 195°F."

# To run:
`python3 readStachiwTable.py`

It will also print out an example ROOT C++ macro and saved as a .C file (plotStachiwCycle1.C for example).
You can also insert the lines for your ROOT C++ code.

The oven should have a uniform temperature distribution.
The temperature fluctuation should be within ±2°C

unit conversion:
```
1 cm = 0.394 inch, 1 inch = 2.54 cm
2 cm = 0.787 inch
2.5 cm = 0.984 inch
1 psi = 0.070 kg/cm2 = 6.89 kPa
200 psi = 14 kg/cm2
```

fast/energy save mode: using the maximum heating and cooling rates provided in the book.
default mode: is conservative mode, the heating and cooling rates are rounded to smaller values, or floor() number.

# Example to show how it works:
```
*************************************
Set mode (conservative or fast)
------- choose the mode carefully -------
press 'enter': conservative mode (by default)
press 'f': fast (energy-save) mode
press:f
Set to fast mode. Warning: use the rate close to the maximum rate, be careful.
*************************************
Set the room/ambient temperature (27 °C as default):
------- choose the season -------
press 'enter': default (27°C)
press 'a': spring/autumn (20°C)
press 'b': summer (30°C)
press 'c': winter (5°C)
or enter a temperature value: (in °C)
press/enter:12
room temperature is set to 12.0 °C.
*************************************
Set the annealing cycle
------- choose the cycle -------
press 1: cycle 1 (table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, single-layer before machining)
press 2: cycle 2 (same table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, laminated layers
press 3: cycle 3 (table 15.3), laminated-layer after machining)
press:1
!!! Now we are checking with the annealing cycle 1
Enter acrylic thickness in mm: 120
Note: we are using conservative curve (a thicker acrylic curve in data than input).
Extract the curve for 127.0mm
!!!!! max_heatingRate_degC 16.111 suggested 10.0
cooling-to-110degC: 1.667
cooling-to-roomTemp: 2.5
Note: the Stachiw's tables assume a default room temperature 27°C; here we use 12.0°C.
----------------------------------------------------------------
Max oven heating rate to 140°C (value in table):
16.11°C/hour; or 0.27°C/minute or 29°F/hour
Fast (energy-save) oven heating rate to 140°C:
16.0°C/hour; or 0.27°C/minute or 28.8°F/hour
----------------------------------
Time for heating to 140 °C (value in table):
7 hours; or 420 minutes
Fast/energy save time for heating to 140°C:
8.0 hours; or 480.0 minutes
------------------------------------------------------
Hold time at 140 °C:
36 hours; or 2160 minutes
------------------------------------------------------
Approx. cooling rate to 110 °C:
1.67°C/hour; or 0.03°C/minute
or 3.0°F/hour
------------------------------------------------------
Hours to Cool oven to 110 °C:
18 hours; or 1080 minutes
------------------------------------------------------
Hold time at 110 °C:
18 hours
------------------------------------------------------
Max cooling rate to room temperature:
2.5°C/hour; or 0.04°C/minute
or 4.5°F/hour
------------------------------------------------------
Total time expected in Stachiw's table:
112 hours; or 6720 minutes
Total time suggested:
124.0 hours; or 7440.0 minutes
or 5 days and 4.0 hours.
------------------------------------------------------
Note1:Assume room temperature 80 °F (27 °C)
Note2: The temperature of material removed from oven after completion of normalizing cycle cannot exceed the ambient room temperature by 15°F (8 °C)
Note3: If the ambient temperature exceeds 80 °F the time to cool down  (category E) may be reduced by multiplying the temperature difference by the approximate cool down rate for the casting thickness and subtracting these hours from category E.
```

# Updates

Please create issues if anything doesn't work.

A "worker-understandable" schedule table, which shows every steps in a time order, can be added in future.
