import numpy as np
from scipy import interpolate
import logging

class linearInterpolation:
    def __init__(self):

        self.temperature = np.array([-75, -50, -25, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 125, 150, 175, 200, 225, 300, 400, 
        500, 600, 700, 800, 900, 1000, 1100])

        self.density = np.array([1.783, 1.582, 1.422, 1.367, 1.341, 1.316, 1.292, 1.268, 1.246, 1.225, 1.204, 1.184, 1.164, 1.127, 1.093, 1.06,
        1, 0.9467, 0.8868, 0.8338, 0.7868, 0.7451, 0.7078, 0.6168, 0.5238, 0.4567, 0.4043, 0.3626, 0.3289, 0.3009, 0.2773, 0.2571])

        self.dynmcViscosity = ([0.01318, 0.01456, 0.01588, 0.0164, 0.01665, 0.0169, 0.01715, 0.0174, 0.01764, 0.01789, 0.01813, 0.01837, 
        0.0186, 0.01907, 0.01953, 0.01999, 0.02088, 0.02174, 0.02279, 0.0238, 0.02478, 0.02573, 0.02666, 0.02928, 0.03287, 0.03547,
        0.03825, 0.04085, 0.04332, 0.04566, 0.04788, 0.05001])
        
        self.densityFunc = interpolate.interp1d(self.temperature, self.density, bounds_error = True, assume_sorted = True)
        
        self.viscosityFunc = interpolate.interp1d(self.temperature, self.dynmcViscosity, bounds_error = True, assume_sorted = True)

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


        
