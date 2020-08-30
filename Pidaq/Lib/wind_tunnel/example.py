from air_properties import linearInterpolation

interObject = linearInterpolation() # Create the object
x = interObject.interpolateDensity(2.5) # interpolate density at Temperature = 2.5
y = interObject.interpolateViscosity(2.5) # interpolate dynamic viscosity at Temperature = 2.5
print(x) 
print(y)
