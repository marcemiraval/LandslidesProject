"""
Abstract: Operations on slope and landslides inventory data as examples for how to use the core concept 'field'

Use Cases:
- get a binary map corresponding to the landslide inventory
- get weight values based on landslide densities for each class in the slope map. 

Provided data:
Two rasters files corresponding to a landslide inventory map, and a slope map.

Resulting data:
- DBF and XLS files with all the classes in the slope map and their corresponding weight value.
 The fields in these resulting files are: slope, area, and weight.
- a raster file named active, which corresponds to the binary version of the input raster landslide inventory
- a raster file named slope_weight with the resulting weight values

"""

__author__ = "Marcela Suarez"
__copyright__ = "Copyright 2014"
__credits__ = ["Marcela Suarez"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "March 2015"
__status__ = "Development"

import arcpy, Susceptibility
from arcpy import env
from utils import _init_log
from coreconcepts import CcField

class LandslideInventory(CcField): #Subclass of CcField

    def __init__(self, inventory_map):
        self.inventory_map = arcpy.Raster(inventory_map)
        
    def local(self, func_toBinary):
        """
        Assign a new value to each pixel in LandslideInventory based on func. 
        "Local operations
        @param func - the local function to be applied to each value in LandslideInventory
        @return a new inventory raster with binary values.
        """
        active = func_toBinary(self.inventory_map)
        return active
       
class Slope(CcField): #Subclass of CcField

    def __init__(self, activeMap, slopeMap):
        self.activeMap = arcpy.Raster(activeMap)
        self.slopeMap = arcpy.Raster(slopeMap)
        
    def local(self, func_Weight):
        """
        Assign a new value to each pixel in Slope based on func. 
        "Local operations
        @param func - the local function to be applied to each value in Slope
        @return a new raster with weight values and a table with the classes in the
		slope map and their corresponding weight value
        """
        weight_slopemap = func_Weight(self.activeMap, self.slopeMap)
        return weight_slopemap
		
try:
    # Set workspace
    ws = raw_input('You are going to define your workspace environment.\n\n'
                   'Please copy and paste the path of the folder with your data: \n')
    env.workspace = r'%s' % ws
    env.overwriteOutput = True

    # Check out any necessary licenses
    arcpy.CheckOutExtension("spatial")

    # Main():
    log = _init_log("fields")
    active = LandslideInventory("inventory").local(Susceptibility.setActive)
    Slope("active","slope").local(Susceptibility.getWeight)
    print('\nYour final results have been saved in the folder defined as workspace environment.\n\n'
          'Now, you should be able to see the following three files in the folder:\n'
          '- slope_weight (raster file)\n'
          '- slope_weight (dbf file)\n'
          '- slope_weight (xls file)\n')

except:
    print arcpy.GetMessages()



