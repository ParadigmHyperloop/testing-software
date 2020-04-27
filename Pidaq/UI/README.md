# Graphical User Interface Directory Structure

Contains all the code that implements a module graphical user interface that can be used differently depending on the desired project.

*** 

## DTS, WindTunnel, Stability, Vacuum

Contains dash control GUIs for each project, as well as grafana dashbooard .json configurations

***

## Dash Project Structure

Using DTS as an example, however they will all follow a similar structure
```
DTS  
├── dts.py                      # Application entrypoint, used to launch the dash app   
├── dts_dash/                   # Python Package containing all dash layout and callbacks for the dts dash app  
    ├── __init__.py                   
    ├── app.py                      # The dash app that gets imported by callback modules and dts.py  
    ├── assets/                     # Contains bootstrap css framework, and one custom .css file  
        ├── css
        ├── js                            
    ├── layout/                     # Subpackage containing layouts built using dash elements  
        ├── __init__.py                  
        ├── control.py  
        ├── sensor.py  
    ├── callbacks/                  # Subpackage defining dash callbacks for the sensor and control tab  
        ├── __init__.py  
        ├── control_callbacks.py  
        ├── sensors_callbacks.py  
```