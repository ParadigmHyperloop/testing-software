"""Contains class that defines linear interpolation functions for wind tunnel testing

Classes:
    LinearInterpolation
"""

import csv
import logging
import sys
from scipy import interpolate

class LinearInterpolation:
    """Creates linear interpolation functions for density and dynamic viscosity

    This class defines two functions that are used to linearly interpolate
    density (kg/m3) and dynamic viscosity (Pa*S) based on temperature (°C)
    for the purpose of wind tunnel testing.
    
    Attributes:
        densityFunc
        viscosityFunc

    Methods:
        interpolateDensity
        interpolateViscosity
    """

    def __init__(self, path):
        """
        Reads a CSV file to define two functions for density and dynamic
        viscosity that can be used with temperature.  The CSV should have same
        structure as current one in Drive, where the units are in the second row.
        
        Parameters:
            path - path to a CSV file of the air properties
        """
        self.logger = logging.getLogger()

        try:
            open(path) # Open the CSV file
        except IOError as err:
            self.logger.error(err)
            sys.exit()
        with open(path) as file:
            csv_reader= csv.reader(file, delimiter =',')
            next(csv_reader) # Skip the first row
            tempCol, densityCol, viscosityCol = -1,-1,-1
            row = next(csv_reader) # Read the second row that contains the units
        
            count = 0 # For tracking the column index
            for cell in row: # This loop determines the column index for 
                    # temperature, density, and dynamic viscosity based on units

                if cell.find('°C') != -1:
                    tempCol = count

                if cell.find('[kg/m3]') != -1:
                    densityCol = count

                if cell.find('[Pa*S]') != -1:
                    viscosityCol = count
                count += 1

            # if a unit is not found, terminate the script
            if tempCol == -1: 
                self.logger.error('Could not find "°C" in any column header.')
                sys.exit()
            if densityCol == -1: 
                self.logger.error('Could not find "kg/m3" in any column header.')
                sys.exit()
            if viscosityCol == -1:
                self.logger.error('Could not find "Pa*S" in any column header.')
                sys.exit()

            tempList = []
            densityList = []
            viscosityList = []
            for row in csv_reader: # Populate each list with the relevant values casted to float
                tempList.append(float(row[tempCol]))
                densityList.append(float(row[densityCol]))
                viscosityList.append(float(row[viscosityCol]))
            
            # Define the interpolation function for density
            self.densityFunc = interpolate.interp1d(tempList, densityList,
                                                    bounds_error = True, assume_sorted = True)
            
            # Define the interpolation function for viscosity
            self.viscosityFunc = interpolate.interp1d(tempList, viscosityList, 
                                                        bounds_error = True, assume_sorted = True)

    def interpolateDensity(self, inputTemp):
        """Return interpolated value of density based on temperature.
        If temperature is out of bounds, return 0.        
        """
        try:
            value= self.densityFunc(inputTemp)
        except ValueError as e:
           self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
           value = 0
        return value
    
    def interpolateViscosity(self, inputTemp):
        """Return interpolated value of dynamic viscosity based on temperature.
        If temperature is out of bounds, return 0.
        """
        try:
            value= self.viscosityFunc(inputTemp)
        except ValueError as e:
            self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
            value = 0
        return value
        