from Agents.Car import CarAgent
from Agents.TrafficLight import TrafficLightAgent
from Agents.Legend import *


def agent_portrayal(agent):
    """
    This file contains the visual information visualization used to generate the interactive map on the webpage
    """
    if agent is None:
        return
    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }
    if isinstance(agent, CarAgent):
        portrayal["Shape"] = "car.png"
        portrayal["Layer"] = "0"
        return portrayal

    elif isinstance(agent, TrafficLightAgent):
        portrayal["Shape"] = "rect"
        if agent.trafficColor == "red":
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "green"
        portrayal["w"] = "0.5"
        portrayal["h"] = "0.5"
        portrayal["Layer"] = "1"
        return portrayal
    elif isinstance(agent, LegendCarIcon):
        portrayal["Shape"] = "car.png"
        portrayal["Color"] = "black"
        portrayal["Layer"] = "2"
        portrayal["text"] = "                      Car"
        portrayal["w"] = "1"
        portrayal["h"] = "1"
        return portrayal
    elif isinstance(agent, LegendGreenTlightIcon):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["text"] = "                      Green light"
        portrayal["Layer"] = "2"
        portrayal["w"] = "0.5"
        portrayal["h"] = "0.5"
        return portrayal
    elif isinstance(agent, LegendRedTlightIcon):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "red"
        portrayal["text"] = "                      Red light"
        portrayal["Layer"] = "2"
        portrayal["w"] = "0.5"
        portrayal["h"] = "0.5"
        return portrayal
