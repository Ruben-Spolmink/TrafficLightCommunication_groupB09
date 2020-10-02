from Car import CarAgent
from TrafficLight import TrafficLightAgent


def agent_portrayal(agent):
    '''
    This file contains the visual information visualization uses to generate the interactive map on the webpage
    '''
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
