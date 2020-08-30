from air_properties import linearInterpolation

interObject = linearInterpolation() # Create the object
x = interObject.interpolateDensity(-76) # interpolate density
y = interObject.interpolateViscosity(-76) # interpolate dynamic viscosity 
print(x) 
print(y)
