from model import *
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

'''
This file launches the server and the model
'''
#windows code
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#Intersectionmodel = Intersection
#windows code
grid = CanvasGrid(
    agent_portrayal, Intersection().width, Intersection().height, 750, 750
)
server = ModularServer(Intersection, [grid], "Intersectionmodel")
server.port = 8522  # The default
server.launch()
