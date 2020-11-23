GIS Tool for Landslide Susceptibility Assessment
============================================================


Contents

----------------------
- `LandsSuscep_cc.py`: Implementation of Landslides Susceptibility using core concepts.
   This python file contains the definition of two classes in terms of concepts and also it is from here
   where the implementation is tested.   
- `Susceptibility.py`: Implementation of "Susceptibility" using arcpy package. This package is used in "LandsSuscep_cc.py""
- `coreconcepts.py`: Abstract concepts.
- `utils.py`: Utilities.


How to test the code and run the example
=========================================
Dependencies
- [Arcpy] 

Data included as example:

Two raster files are included as example to test the implementation.
1. slope
2. inventory

Instructions:
1. Copy the folder in your computer.
2. Run "LandsSuscep_cc.py"
3. You will be requested to indicate the folder's path. You can just copy and paste it as it is suggested.
4. Check the folder when you have the new output files named slope_weight. (This is also indicated in a final message).



How to test the code with your own data
=========================================
Dependencies
- [Arcpy] 

Data requiered:
- Raster file (ArcGIS format) with slope data of the area of study. The name of this file should be: Slope.
- Raster file (ArcGIS format) with the landslide inventory of the area of study. The name of this file should be inventory. The file should be already reclassified with three classes: "Body", "Scarp", and "NoActivity"

Steps:
1. Copy the python file in the folder with your data.
2. Run "LandsSuscep_cc.py"
3. You will be requested to indicate the folder's path. You can just copy and paste it as it is suggested.
4. Check the folder when you have the new output files named slope_weight. (This is also indicated in a final message).

