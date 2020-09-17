from Model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(Intersection,
                       [grid],
                       "Intersection",
                       {"width":10, "height":10})
server.port = 8521 # The default
server.launch()
