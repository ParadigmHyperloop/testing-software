# Pidaq (Rasp Pi Data Aquisitor) 

This directory contains all of the code that will run on the raspberry pi. The pi will receive and parse CAN messages containing raw telemetry, apply calculations,  and create a packet(s) containing either a JSON or protobuf message to send to the control laptop via ethernet (UDP)
 
# Development
We will be using docker to cross compile c++ for the raspberry pi

Ensure docker is installed and running on your machine. Windows 10 Home does not have proper support for docker, however MUN offers a free upgrade to windows 10 education which is fully featured. The update is easy, unintrusive, and tasks less than 1 hour.

## Taskrunner Setup Code for VsCode
* Install vscode extension "Tasks" by actboy 168

* Open testing-software/Pidaq folder with vscode

* Replace the folder path in .vscode/tasks.json line 28 command: `compile and run Pidaq HelloWorld`, with your path. replace this -> `/c/Hyperloop/testing-software/Pidaq `

* Try the task buttons in blue taskbar at bottom of vscode window:
    * `echoTest` should print Hello taskrunner good.
    * `buildPiImage` should build docker image `pidaq:v1`
    * `compileRunPiHelloWorld` should print "---Hello Paradigm!!!---"
