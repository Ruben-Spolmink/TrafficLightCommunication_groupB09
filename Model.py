import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Car import CarAgent
from TrafficLight import TrafficLight
from Portrayal import agent_portrayal
spawnchance = 3 #this should be an parameter in model interface
NumberOfAgents = 0




def readroadmap():
    filepath = 'Generatedmap.txt'
    roadmap = []
    spawns = []
    lights = []
    run = 0
    with open(filepath, 'r') as roadmapfile:
        text = roadmapfile.readlines()
        header = text[0:4]
        info = header[0].split(",")
        cellsperlane = int(info[0].strip())
        gridsize = int(info[1].strip())
        streetlength = int(info[2].strip())
        intersections = int(info[3].strip())
        text = text[4:]
        height = (len(text[0].split(",")))
        for y, line in enumerate(text):
            road = line.strip().split(',')
            roadmap.append(road)
            for x, tile in enumerate(road):
                if tile.startswith("C"):
                    spawns.append([[x, y], tile])
                if tile.startswith("T"):
                    lights.append([[x, y], tile])
                    run += 1
    return roadmap, spawns, lights, height, cellsperlane


class Intersection(Model):
    def __init__(self):
        global NumberOfAgents
        self.schedule = RandomActivation(self)
        [self.roadmap, self.spawns, self.lights, self.height, self.cellsperlane] = readroadmap()
        self.width = self.height
        self.grid = MultiGrid(self.width, self.height, True)
        self.running = True
        self.tlightmatrix = np.empty((len(self.lights), len(self.lights)))
        self.tlightmatrix[:] = np.nan
        self.trafficlightlist = []

        for i, light in enumerate(self.lights):
            location = light[0]
            xlocation = int(location[0])
            ylocation = self.height-1-int(location[1])
            trafficlight = TrafficLight(f"{i},{xlocation},{ylocation},{light[1][1:3]}", self,"red")
            self.trafficlightlist.append(f"{i},{xlocation},{ylocation},{light[1][1:3]}")
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

        self.tlightmatrix = self.lighttransfermatrix()

    def lighttransfermatrix(self):
        for agent in self.trafficlightlist:
            # determine which traffic lights go where
            # replace self.tlightmatrix [from,to]'s with 0 in that case
            pass



    def step(self):
        global spawnchance
        global NumberOfAgents
        for spawn in self.spawns:
            if random.randint(0, 100) < spawnchance:
                location = spawn[0]
                xlocation = int(location[0])
                ylocation = self.height-1-int(location[1])
                direction = spawn[1][1]
                car = CarAgent(NumberOfAgents, self, 1, direction,[xlocation, ylocation], self.lane)
                NumberOfAgents += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()

