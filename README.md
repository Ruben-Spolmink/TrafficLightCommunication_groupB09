# DOMAS_groupB09
![Gif of environment](intersection.gif | width=48)
muti agent system project

To run the file call Visualizaiion.py. This file will launch a webpage where the user can interact

The model is a traffic model where cars will drive in a grid with 4 connected intersections
A car is represented by a cartoon car icon and a traffic light is a colored square with red being the light red and green if the light is green

The cars are randomly spawned at the edges of the intersections and when they reach an edge will be deleted
The cars can also drive around from intersection to intersection and will follow correct lanes. They will also abide to the traffic light

The traffic light contain a basic schedule that control the flow of traffic

The goal of the model is to test different strategies for traffic light and see if they can reduce pollution by cars
The cars will polute more if they slow down and need to accelerate again, so we want to minimize the wait time while minimize wait time as much as possible.
