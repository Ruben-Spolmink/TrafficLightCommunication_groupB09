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
        cellsperlane = int(float(header[0].split("=")[1].strip()))
        gridsize = int(float(header[1].split("=")[1].strip()))
        streetlength = int(float(header[2].split("=")[1].strip()))
        intersections = int(float(header[3].split("=")[1].strip()))
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
        self.blok = ""
        self.route = []

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
            if(ylocation < self.height/2):
                #we can assume the car is placed on the bottom half the intersection
                if(xlocation < self.width/2):
                    #we can assume that the car is placed on the left half of the screen
                    self.blok = "A"
                else:
                    #the car is placed on the right half of the screen
                    self.blok = "B"
            if(ylocation > self.height/2):
                #we can assume the car is placed on the top half of the screen
                if(xlocation < self.width/2):
                    #we can assume that the car is placed on the left half of the screen
                    self.blok = "C"
                else:
                    #we can assume that the car is on the right half of the screen
                    self.blok = "D"

            self.route = self.generateRoute(self.direction, self.blok, random.randint(0,4))
            car = CarAgent(NumberOfAgents, self, 1, self.direction, [xlocation, ylocation], self.lane, self.blok, self.route)
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


    def generateRoute(self,direction,blok,n_intersections):
        route = []
        #dictionary with options for direcitons when wanting to move to another intersection
        route_stay = {"A":["N","E"],
                      "B":["W","N"],
                      "C":["S","E"],
                      "D":["S","W"]}
        #dictionary with options for directions when leaving the instersecion
        route_leave = {"A":["S","W"],
                      "B":["E","S"],
                      "C":["N","W"],
                      "D":["N","E"]}

        calculation_dictornary = {"A": {"N" : "C",
                                        "E" : "B"},
                                  "B": {"W" : "A",
                                        "N" : "D"},
                                  "C": {"S" : "A",
                                        "E" : "D"},
                                  "D": {"S" : "B",
                                        "W" : "C"}}

        for i in range(n_intersections):
            #start with a all the options enabled
            options = ["N","E","S","W"]
            if direction in options: options.remove(direction) #removes the direction the car came from since we cannot make u-turn
            if(i < n_intersections): #check if we are leaving the intersecions or that we are going towards another intesection
                for option in route_leave[blok]:
                    if option in options: options.remove(option) #if we want to go to the next intersection we remove the options where we leave the instersection
            else:
                for option in route_stay[blok]:
                    if option in options: options.remove(option) #if we want to leave the intersecions we remove the options where we stay on the intersecion
            new_choice = random.choice(options) #we pick a random option from the options that are left
            route.append(new_choice) #add the option to the route we take
            direction = new_choice #set direction as if we are in the next step of the route
            if(i < n_intersections): #if we go to another intersecion we need to calculate the blok we are going to
                blok = calculation_dictornary[blok][direction]#add the intersection blok as if we are in the next intersecion
        return route
        #calculate where we end up if we add current blok plus the direction


    def step(self):
        global spawnchance
        global NumberOfAgents
        for spawn in self.spawns:
            if random.randint(0, 100) < spawnchance:
                location = spawn[0]
                xlocation = int(location[0])
                ylocation = self.height-1-int(location[1])
                direction = spawn[1][1]
                if(ylocation < self.height/2):
                #we can assume the car is placed on the bottom half the intersection
                    if(xlocation < self.width/2):
                    #we can assume that the car is placed on the left half of the screen
                        self.blok = "A"
                    else:
                    #the car is placed on the right half of the screen
                        self.blok = "B"
                if(ylocation > self.height/2):
                #we can assume the car is placed on the top half of the screen
                    if(xlocation < self.width/2):
                    #we can assume that the car is placed on the left half of the screen
                        self.blok = "C"
                    else:
                    #we can assume that the car is on the right half of the screen
                        self.blok = "D"
                self.route = self.generateRoute(self.direction, self.blok, random.randint(0,4))
                car = CarAgent(NumberOfAgents, self, 1, direction,[xlocation, ylocation], self.lane, self.blok, self.route)
                NumberOfAgents += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()
