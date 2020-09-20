from Car import CarAgent
from TrafficLight import TrafficLight


def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }
    if isinstance(agent, CarAgent):
        portrayal["Color"] = "blue"
        portrayal["r"] = "0.5"
        portrayal["Layer"] = "0"
        return portrayal


    elif isinstance(agent, TrafficLight):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["w"] = "0.5"
        portrayal["h"] = "0.5"
        portrayal["Layer"] = "0"
        return portrayal
