"""
Abstract: Implementation a library called "Susceptibility" using arcpy package

"""
__author__ = "Marcela Suarez"
__copyright__ = "Copyright 2014"
__credits__ = ["Marcela Suarez"]


import arcpy, math
from arcpy.sa import *
from arcpy import env

def setActive(inventory): # Reclass Inventory
     active = Reclassify(inventory, "INVENTORY", RemapValue([["Body",1],["Scarp",1],["NoActivity",0]]))
     active.save("active")

def getWeight(slopemap, activemap): # Compute weights based on landslide density.

	# Execute Combine
     outCombine = Combine([slopemap, activemap])
     outCombine.save("outCombine") # Save the output
	 
	 
     # Calculate areas from outCombine
     # Create new field to cast field "COUNT", which contains the number of pixels
     arcpy.AddField_management(outCombine, "COUNT_","DOUBLE") # add field
     arcpy.CalculateField_management(outCombine,"COUNT_",'!COUNT!',"PYTHON_9.3")
          
     # Compute areas for outcombine raster
     arcpy.AddField_management(outCombine,"AREA","DOUBLE")
     arcpy.CalculateField_management(outCombine, "AREA","!COUNT_!*10.4*10.4","PYTHON") # Compute Area
     
     # Calculate the area with active landslides in each slope class 
     arcpy.AddField_management(outCombine, "AREA_ACT","DOUBLE") # add field 

     # Set local variables
     myexpression = "getAreaAct(!AREA!,!ACTIVE!)" 
     codeblock = """def getAreaAct(AREA, ACTIVE):  
          if ACTIVE == 1:
               return AREA
          else:
               return 0"""
     arcpy.CalculateField_management(outCombine, "AREA_ACT", myexpression, "PYTHON",codeblock)
    
	 # Search cursor to calculate total areas 
     outCombine.save("Slope_Weight")
     # for r in arcpy.da.SearchCursor(locRas1, ["VALUE", "COUNT"]): 
     fields = ['SLOPE','AREA_ACT']
     slopeAct = {slope:0 for slope in range(1,8)}
     with arcpy.da.SearchCursor("Slope_Weight", fields) as cursor:
               for row in cursor:
                    slopeAct[row[0]] += row[1]
     arcpy.AddField_management("Slope_Weight", "AREACLASSACT","DOUBLE") # add field

     # Assign values to new field
     fields = ['SLOPE','AREACLASSACT']
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursorU:
          for row in cursorU:
               row[1] = slopeAct[row[0]]
               cursorU.updateRow(row)
               
     # Calculate the total area in each slope class 
     # Search cursor to calculate total areas 
     fields = ['SLOPE','AREA']
     slopeAreas = {slope:0 for slope in range(1,8)}
     with arcpy.da.SearchCursor("Slope_Weight", fields) as cursor:
          for row in cursor:
               slopeAreas[row[0]] += row[1]
     arcpy.AddField_management("Slope_Weight", "AREACLASSTOT","DOUBLE") # add field
	 
     # Assign values to new field
     fields = ['SLOPE','AREACLASSTOT']
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursorU:
          for row in cursorU:
               row[1] = slopeAreas[row[0]]
               cursorU.updateRow(row)

     # Calculate the total active area in the map
     fields = ['ACTIVE','AREA']
     ActiveArea = 0
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursor:
          for row in cursor:
               if (row[0] == 1):
                    ActiveArea += row[1]
     arcpy.AddField_management("Slope_Weight", "AREACTOT","DOUBLE") # add field

     # assign values to new field
     fields = ['AREACTOT']
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursor2:
          for row in cursor2:
               row[0] = ActiveArea
               cursor2.updateRow(row)
        
     # Calculate the total area in the map
     fields = ['AREA']
     TotalArea = 0
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursor:
          for row in cursor:
               TotalArea += row[0]

     arcpy.AddField_management("Slope_Weight", "AREAMAPTOT","DOUBLE") # add field

     # Assign values to new field
     fields = ['AREAMAPTOT']
     with arcpy.da.UpdateCursor("Slope_Weight", fields) as cursor2:
          for row in cursor2:
               row[0] = TotalArea
               cursor2.updateRow(row)

			   
     # Calculate densities in outCombine
     # Calculate the landslide density per slope class
     arcpy.AddField_management("Slope_Weight", "DENSCLASS","DOUBLE") # add field     

     # Set local variables
     myexpression = "getAreaAct(!AREACLASSACT!,!AREACLASSTOT!)" 
     codeblock = """def getAreaAct(AREACLASSACT, AREACLASSTOT):  
               return AREACLASSACT/AREACLASSTOT"""
     arcpy.CalculateField_management("Slope_Weight", "DENSCLASS", myexpression, "PYTHON",codeblock)


     # Calculate the landslide density for the entire map
     arcpy.AddField_management("Slope_Weight", "DENSMAP","DOUBLE") # add field  

     # Set local variables
     myexpression = "getAreaAct(!AREACTOT!,!AREAMAPTOT!)" 
     codeblock = """def getAreaAct(AREACTOT, AREAMAPTOT):  
               return AREACTOT/AREAMAPTOT"""
     arcpy.CalculateField_management("Slope_Weight", "DENSMAP", myexpression, "PYTHON",codeblock)


     # Calculate weights
     arcpy.AddField_management("Slope_Weight", "WEIGHT","DOUBLE") # add field

     # Set local variables
     myexpression = "getAreaAct(!DENSCLASS!,!DENSMAP!)" 
     codeblock = """def getAreaAct(DENSCLASS, DENSMAP):  
          return math.log(DENSCLASS/DENSMAP)"""
     arcpy.CalculateField_management("Slope_Weight", "WEIGHT", myexpression, "PYTHON",codeblock)

	 
     # Exporting final results to table
     arcpy.TableToTable_conversion("Slope_Weight",env.workspace,"slope_weights")
     arcpy.DeleteIdentical_management("slope_weights.dbf","WEIGHT")
     arcpy.DeleteField_management("slope_weights.dbf",["ACTIVE","COUNT_","AREA_ACT","AREACLASSA","AREACLASST","AREAMAPTOT","AREACTOT","DENSCLASS","DENSMAP"])
     arcpy.TableToExcel_conversion("slope_weights.dbf","slope_weights.xls")
	 
	 
	 # Execute Delete
     arcpy.Delete_management("outCombine")
     arcpy.Delete_management("active")
