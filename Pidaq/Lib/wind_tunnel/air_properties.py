import numpy as np
from scipy import interpolate
import logging
import csv
import sys

class linearInterpolation:

    def __init__(self, path):
        self.logger = logging.getLogger()
        with open(path) as file: # Open the csv file
            csv_reader= csv.reader(file, delimiter =',')
            next(csv_reader) # Skip the first row
            tempCol, densityCol, viscosityCol = -1,-1,-1
            row = next(csv_reader) # Read the second row that contains the units
        
            count = 0 # For tracking the column index
            for cell in row: # This loop determines the column index for 
                    # temperature, density, and dynamic viscosity based on units
    
                # if the cell contains °C, store its index
                if cell.find('°C') != -1:
                    tempCol = count

                if cell.find('[kg/m3]') != -1:
                    densityCol = count

                if cell.find('[Pa*S]') != -1:
                    viscosityCol = count
                count += 1

            if tempCol == -1: # if °C is not in any column header, terminate the script
                self.logger.error("Could not find \"°C\" in any column header.")
                sys.exit()
            if densityCol == -1: 
                self.logger.error("Could not find \"kg/m3\" in any column header.")
                sys.exit()
            if viscosityCol == -1:
                self.logger.error("Could not find \"Pa*S\" in any column header.")
                sys.exit()

            tempList = []
            densityList = []
            viscosityList = []
            for row in csv_reader: # Populate each list with the relevant values casted to float
                tempList.append(float(row[tempCol]))
                densityList.append(float(row[densityCol]))
                viscosityList.append(float(row[viscosityCol]))
            
            # Create the interpolation function for density
            self.densityFunc = interpolate.interp1d(tempList, densityList,
                                                    bounds_error = True, assume_sorted = True)
            
            # Create the interpolation function for viscosity
            self.viscosityFunc = interpolate.interp1d(tempList, viscosityList, 
                                                      bounds_error = True, assume_sorted = True)

    def interpolateDensity(self, inputTemp):
        try:
            value= self.densityFunc(inputTemp)
        except ValueError as e:
           self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
           value = 0
        return value
    
    def interpolateViscosity(self, inputTemp):
        try:
            value= self.viscosityFunc(inputTemp)
        except ValueError as e:
            self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
            value = 0
        return value