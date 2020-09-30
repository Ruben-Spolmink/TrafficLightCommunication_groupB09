from model import *
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

Intersectionmodel = Intersection

grid = CanvasGrid(agent_portrayal, Intersectionmodel().width, Intersectionmodel().height, 750, 750)
server = ModularServer(Intersectionmodel,
                       [grid],
                       "Intersectionmodel"
                       )
server.port = 8522  # The default
server.launch()
