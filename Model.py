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
    filepath = 'roadmap.txt'
    roadmap = []
    spawns = {}
    lights = {}
    run = 0
    with open(filepath, 'r') as roadmapfile:
        text = roadmapfile.readlines()
        for x, line in enumerate(text):
            road = line.strip().split(',')
            roadmap.append(road)
            for y, tile in enumerate(road):
                if tile.startswith("c"):
                    spawns[tile] = [x, y]
                if tile.startswith("l"):
                    lights[run] = [x, y]
                    run +=1
    return roadmap, spawns, lights



class Intersection(Model):
    def __init__(self, height=10, width=10): #should change so height and widht are same as Generatedmap
        global NumberOfAgents
        self.height = height
        self.width = width
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        [self.roadmap, self.spawns, self.lights] = readroadmap()
        self.running = True

        for light in self.lights:
            location = self.lights[light]
            xlocation = width-1-int(location[0])
            ylocation = height-1-int(location[1])
            trafficlight = TrafficLight(NumberOfAgents, self,"red")
            NumberOfAgents += 1
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))
            print("placed_traffic_agent")


        for spawn in self.spawns:
            direction = spawn[1]
            location = self.spawns[spawn]
            xlocation = width-1-int(location[0])
            ylocation = height-1-int(location[1])
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
            car = CarAgent(NumberOfAgents, self, 1, "n",[xlocation, ylocation])
            NumberOfAgents += 1
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()
