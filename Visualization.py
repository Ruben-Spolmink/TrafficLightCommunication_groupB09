from Model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

grid = CanvasGrid(agent_portrayal, 8, 8, 500, 500)
server = ModularServer(Intersection,
                       [grid],
                       "Intersection",
                       {"width":8, "height":8})
server.port = 8521 # The default
server.launch()