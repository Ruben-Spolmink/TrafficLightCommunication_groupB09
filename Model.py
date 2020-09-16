from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def readroadmap():
    filepath = '/home/jordi/Desktop/roadmap.txt'
    roadmap = []
    spawns = {}
    with open(filepath, 'r') as roadmapfile:
        text = roadmapfile.readlines()
        for x, line in enumerate(text):
            road = line.strip().split(',')
            roadmap.append(road)
            for y, tile in enumerate(road):
                if tile.startswith("c"):
                    spawns[tile] = [x, y]

    return roadmap, spawns


class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, goal, nextlane):
        super().__init__(name, model)
        self.speed = speed
        self.direction = direction
        self.goal = ""
        self.nextlane = ""

    def step(self):
        pass


class Intersection(Model):
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        [self.roadmap, self.spawns] = readroadmap()

        for i, spawn in enumerate(self.spawns):
            direction = spawn[1]
            location = self.spawns[spawn]
            xlocation = width-1-int(location[0])
            ylocation = height-1-int(location[1])
            car = CarAgent(i, self, 1, direction,  "", "")
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))


def agent_portrayal(CarAgent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5,
                 "Color": "red",
                 "Layer": 0}
    return portrayal



