from model import *
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Legend import *

"""
This file launches the server and the model, if on windows there might be issues with tornado. 
Uncomment the code to fix this.
"""
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

grid = CanvasGrid(
    agent_portrayal, Intersection().width, Intersection().height, 1000, 1000
)
server = ModularServer(Intersection, [grid], "Intersectionmodel")
server.port = 8520  # The default
server.launch()
