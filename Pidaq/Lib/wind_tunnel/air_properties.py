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

    def __init__(self, path: str):
        """
        Reads a CSV file to define two functions for density and dynamic
        viscosity that can be used with temperature.  The CSV should have same
        structure as current one in Drive, where the units are in the second row.
        
        Parameters:
            path - path to a CSV file of the air properties

        Raises:
            ValueError - A unit (hence the column for a property) was not found
        """
        self.init(path)
        

    def init(self, path: str):
            self.logger = logging.getLogger()

            try:
                open(path)
            except FileNotFoundError as err:
                self.logger.error(err)
                return 0

            with open(path) as file:
                csv_reader = csv.reader(file, delimiter =',')
                next(csv_reader) # Skip the first row
                row = next(csv_reader) # Read the second row that contains the units
                tempCol, densityCol, viscosityCol = -1,-1,-1

                # This loop determines the column indices based on units
                for index, cell in enumerate(row): 

                    if cell.find('°C') != -1:
                        tempCol = index

                    if cell.find('[kg/m3]') != -1:
                        densityCol = index

                    if cell.find('[Pa*S]') != -1:
                        viscosityCol = index

                # If a unit was not found, raise an error
                if tempCol == -1: 
                    raise ValueError('Temperature unit "°C" was not found.')
                    
                if densityCol == -1: 
                    raise ValueError('Density unit "kg/m3" was not found.')
                    
                if viscosityCol == -1:
                    raise ValueError('Dynamic viscosity unit "Pa*S" was not found.')

                tempList = []
                densityList = []
                viscosityList = []
                for row in csv_reader: # Populate each list with the relevant values casted to float
                    tempList.append(float(row[tempCol]))
                    densityList.append(float(row[densityCol]))
                    viscosityList.append(float(row[viscosityCol]))
                
                # Define the interpolation function for density
                self.densityFunc = interpolate.interp1d(tempList,
                                                        densityList,
                                                        bounds_error = True,
                                                        assume_sorted = True)
                
                # Define the interpolation function for viscosity
                self.viscosityFunc = interpolate.interp1d(tempList,
                                                        viscosityList, 
                                                        bounds_error = True,
                                                        assume_sorted = True)

    def interpolateDensity(self, inputTemp: float) -> float:
        """Return interpolated value of density based on temperature.
        If temperature is out of bounds, return 0.      
        """
        try:
            value = self.densityFunc(inputTemp)
        except ValueError as e:
           self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
           value = 0
        return value
    
    def interpolateViscosity(self, inputTemp: float) -> float:
        """Return interpolated value of dynamic viscosity based on temperature.
        If temperature is out of bounds, return 0.
        """
        try:
            value = self.viscosityFunc(inputTemp)
        except ValueError as e:
            self.logger.warning("Temperature out of bounds, returning 0. " + str(e))
            value = 0
        return value
        