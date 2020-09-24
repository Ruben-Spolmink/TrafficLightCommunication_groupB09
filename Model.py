import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Car import CarAgent
from TrafficLight import TrafficLight
from Portrayal import agent_portrayal
spawnchance = 3 #this should be an parameter in model interface
NumberOfAgents = 0


def readroadmap(): #needs to correctly read in roadmapfile
    filepath = 'Generatedmap.txt'
    roadmap = []
    spawns = []
    lights = []
    run = 0
    with open(filepath, 'r') as roadmapfile:
        text = roadmapfile.readlines()
        height = (len(text[0].split(",")))
        for y, line in enumerate(text):
            road = line.strip().split(',')
            roadmap.append(road)
            for x, tile in enumerate(road):
                if tile.startswith("C"):
                    spawns.append([[x, y], tile])
                if tile.startswith("T"):
                    lights.append([[x, y], tile])
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
            location = light[0]
            xlocation = int(location[0])
            ylocation = self.height-1-int(location[1])
            trafficlight = TrafficLight(NumberOfAgents, self,"red")
            NumberOfAgents += 1
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))
            print("placed_traffic_agent")

        for spawn in self.spawns:
            self.direction = spawn[1][1]
            self.lane = spawn[1][2]
            location = spawn[0]
            xlocation = int(location[0])
            ylocation = self.height-1-int(location[1])
            car = CarAgent(NumberOfAgents, self, 1, self.direction, [xlocation, ylocation], self.lane)
            NumberOfAgents += 1
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))
            print("placed_car")

    def step(self):
        global spawnchance
        global NumberOfAgents
        for spawn in self.spawns:
            if random.randint(0, 100) < spawnchance:
                # if it is possible to spawn a car (NEEDS TO BE IMPLEMENTED)
                location = spawn[0]
                xlocation = int(location[0])
                ylocation = self.height-1-int(location[1])
                direction = spawn[1][1]
                car = CarAgent(NumberOfAgents, self, 1, direction,[xlocation, ylocation], self.lane)
                NumberOfAgents += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()
