import numpy as np
from scipy import interpolate
import logging
import csv

class linearInterpolation:
    def __init__(self, path):
        
        # Open the csv file
        with open(path) as file:
            csv_reader= csv.reader(file, delimiter =',')
            next(csv_reader) # Skip the first row
            tempCol, densityCol, viscosityCol = 0,0,0
            row = next(csv_reader) # Read the second row that contains the units
        
            count = 0        # For tracking the column index
            for cell in row: # This loop determines the column index of temperature, density, and dynamic viscosity
                
                # if the cell contains °C
                if cell.find('°C') != -1:
                    tempCol = count

                if cell.find('kg/m3') != -1:
                    densityCol = count

                if cell.find('Pa*S') != -1:
                    viscosityCol = count
                count += 1

            self.tempList = []
            densityList = []
            self.viscosityList = []
            for row in csv_reader: # Populate each list with the relevant values casted to float
                self.tempList.append(float(row[tempCol]))
                densityList.append(float(row[densityCol]))
                self.viscosityList.append(float(row[viscosityCol]))
            
            # Create the interpolation function for density
            self.densityFunc = interpolate.interp1d(self.tempList, densityList, bounds_error = True, assume_sorted = True)
            
            # Create the interpolation function for viscosity
            self.viscosityFunc = interpolate.interp1d(self.tempList, self.viscosityList, bounds_error = True, assume_sorted = True)

    def interpolateDensity(self, inputTemp):
        logger = logging.getLogger()
        try:
            value= self.densityFunc(inputTemp)
        except ValueError as e:
           logger.error("Temperature out of bounds, returning 0. " + str(e))
           value = 0
        return value
    
    def interpolateViscosity(self, inputTemp):
        logger = logging.getLogger()
        try:
            value= self.viscosityFunc(inputTemp)
        except ValueError as e:
            logger.error("Temperature out of bounds, returning 0. " + str(e))
            value = 0
        return value


        
