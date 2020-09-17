from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Car import CarAgent
from TrafficLight import TrafficLight
from Portrayal import agent_portrayal

def readroadmap():
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
        self.height = height
        self.width = width
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        [self.roadmap, self.spawns, self.lights] = readroadmap()

        for i, light in enumerate(self.lights):
            location = self.lights[light]
            xlocation = width-1-int(location[0])
            ylocation = height-1-int(location[1])
            trafficlight = TrafficLight(i, self,"")
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))
            print("placed_traffic_agent")



        for i, spawn in enumerate(self.spawns):
            direction = spawn[1]
            location = self.spawns[spawn]
            xlocation = width-1-int(location[0])
            ylocation = height-1-int(location[1])
            car = CarAgent(i, self, 1, direction,  "", "")
            self.schedule.add(car)
            self.grid.place_agent(car, (xlocation, ylocation))
            print("placed_car")
