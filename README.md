# Pollution reduction by communicating trafficlights
![Gif of environment](Images/intersection.gif)

## Overview
This project investigates the pollution reduction by communicating traffic lights in a multi-intersection environment.
The model contains traffic light agents which are able to communicate with each other as well as cars which drive
around by themselves, without any communication. The cars will follow the direction of the lane they are in and will
choose a random lane when they take a turn or go straight at the traffic lights.  <br/> 
This repository contains code to generate a map with x^2 intersections (roadmapgenerator.py) and code that
 visualizes the environment and runs the simulation (Run.py). This script launches a webpage with 
 the visualization.
<br/> 
NOTE: One important thing to note is that each iteration in the model is equal to 0.2 seconds in real life.
This is done in order to prevent the cars from skipping tiles.
## Scripts
- Generating the map: <br/> 
Command: roadmapgenerator.py gridsize streetlength #intersections <br/> 
NOTE: there is already a pregenerated environment ./textfiles/Generatedmap.txt<br/>
The gridsize corresponds to the size of the grid compared to real life, the street length is the length from 1
intersection to another, the #intersections in the number of intersections. 
The measures are in cm (e.g. a gridsize of 300 is a 3m x 3m grid). The number of intersections needs to be X^2 
where X is an integer. Currently there is only visualization support for a gridsize of 300. This script will generate 
Generatedmap.txt file which will be used for visalization.
- Running the simulation: <br/> 
Command: Run.py<br/> 
This will open a webbrowser with the visualized simulation.<br/> 
Click start to start the simulation. In order to change parameters,
change the parameters in the visualization and click reset. 
The emission is shown in the graphs below the simulation. 
- Running a batch of simulations: <br/>
Command: Run.py Batch<br/>
The parameters for the batchrun are specified in the batcnrun function in model.py. Change the parameters 
and the filename there in order to run the right batch. This will output the file in Data.csv which can be
loaded in for example a pandas dataframe.
## Parameters
In the visualization as well as in the batch run there are 4 different parameters: 
offset, tactic, cycletime and spawnrate.<br/>
- Offset: Only works with the offset tactic. This gives all the adjacent trafficlights an offset in their 
sequence of turning green. In the case of 4 intersections, intersection 0 and 3 behave the same and 1 and 2 
behave the same.
- Tactic: Choose between 4 tactics. More about the tactics can be read in the report.
- Cycletime: Choose for what number of iterations the light stays green.
- Spawnrate: Choose what the chance is for a car to spawn for every spawning location at each iteration. 