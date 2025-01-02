# acrylic_annealing
Stachiw acrylic annealing

python3 readStachiwTable.py
It will also print out an example ROOT C++ macro.
Insert the lines for any ROOT C++ code.

The oven should have a uniform temperature distribution.
The temperature fluctuation should be within ±2°C

unit conversion:
1 cm = 0.394 inch, 1 inch = 2.54 cm
2 cm = 0.787 inch
2.5 cm = 0.984 inch
1 psi = 0.070 kg/cm2 = 6.89 kPa
200 psi = 14 kg/cm2

- Example and how it works:

*************************************
Set mode (conservative or fast)
------- choose the mode carefully -------
press 'enter': conservative mode (by default)
press 'f': fast (energy-save) mode
press:
Use conservative mode (by default)
*************************************
Set the room/ambient temperature (27 °C as default):
------- choose the season -------
press 'enter': default (27°C)
press 'a': spring/autumn (20°C)
press 'b': summer (30°C)
press 'c': winter (5°C)
or enter a temperature value: (in °C)
press:
room temperature is set to 27°C by default
*************************************
Set the annealing cycle
------- choose the cycle -------
press 1: cycle 1 (table 15.1) NORMALIZING SCHEDULE FOR ACRYLIC CASTINGS, single-layer before machining)
press 2: cycle 2 (
press 3: cycle 3 (laminated-layer after machining)
press:1
Enter acrylic thickness in mm: 50
50.0mm is less than the minimum 50.8mm in Stachiw's database.
Use the 50.8mm curve [definitely safe].
Note: we are using conservative curve (a thicker acrylic curve in data than input).
Extract the curve for 50.8mm







