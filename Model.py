import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Car import CarAgent
from TrafficLight import TrafficLight
from Portrayal import agent_portrayal
agents_per_tick = 3 #this should be an parameter in model interface
NumberOfAgents = 0


def readroadmap(): #needs to correctly read in roadmapfile
    filepath = 'Generatedmap.txt'
    roadmap = []
    spawns = {}
    lights = {}
    run = 0
    with open(filepath, 'r') as roadmapfile:
        text = roadmapfile.readlines()
        height = (len(text[0].split(",")))
        for x, line in enumerate(text):
            road = line.strip().split(',')
            roadmap.append(road)
            for y, tile in enumerate(road):
                if tile.startswith("C"):
                    spawns[tile] = [x, y]
                if tile.startswith("T"):
                    lights[run] = [x, y]
                    run +=1
    return roadmap, spawns, lights, height


class Intersection(Model):
    def __init__(self): #should change so height and widht are same as Generatedmap
        global NumberOfAgents
        self.schedule = RandomActivation(self)
        [self.roadmap, self.spawns, self.lights, self.height] = readroadmap()
        self.width = self.height
        self.grid = MultiGrid(self.width, self.height, True)
        self.running = True

        for light in self.lights:
            location = self.lights[light]
            xlocation = self.width-1-int(location[0])
            ylocation = self.height-1-int(location[1])
            trafficlight = TrafficLight(NumberOfAgents, self,"red")
            NumberOfAgents += 1
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))
            print("placed_traffic_agent")


        for spawn in self.spawns:
            direction = spawn[1]
            location = self.spawns[spawn]
            xlocation = self.width-1-int(location[0])
            ylocation = self.height-1-int(location[1])
            car = CarAgent(NumberOfAgents, self, 1, direction,[xlocation, ylocation])
            NumberOfAgents += 1
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))
            print("placed_car")

    def step(self):
        global agents_per_tick
        global NumberOfAgents
        for i in range(agents_per_tick):
            xlocation = self.random.randrange(self.grid.width)
            ylocation = self.random.randrange(self.grid.height)
            car = CarAgent(NumberOfAgents, self, 1, "N",[xlocation, ylocation])
            NumberOfAgents += 1
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()
