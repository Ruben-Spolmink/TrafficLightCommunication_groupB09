import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
import math
from Car import CarAgent
from TrafficLight import TrafficLightAgent

SPAWNCHANCE = 3  # this should be an parameter in model interface



# creates a np array where all 0's are connections that go from row to column
def lightconnection(lightmatrix, trafficlightlist, intersections):
    for trafficlightfrom in trafficlightlist:
        direction = trafficlightfrom[0][1:3]
        intersection = int(trafficlightfrom[0][3])
        if direction in ["NL", "WD", "SR"]:
            goestointersection = intersection - 1
            if (
                goestointersection > -1
                and (intersection % int(math.sqrt(intersections))) != 0
            ):
                for trafficlightto in trafficlightlist:
                    direction = trafficlightto[0][1]
                    intersection = int(trafficlightto[0][3])
                    if intersection == goestointersection and direction == "W":
                        lightmatrix[
                            int(trafficlightfrom[1]), int(trafficlightto[1])
                        ] = int(0)
        if direction in ["EL", "ND", "WR"]:
            goestointersection = intersection - int(math.sqrt(intersections))
            if goestointersection >= 0:
                for trafficlightto in trafficlightlist:
                    direction = trafficlightto[0][1]
                    intersection = int(trafficlightto[0][3])
                    if intersection == goestointersection and direction == "N":
                        lightmatrix[
                            int(trafficlightfrom[1]), int(trafficlightto[1])
                        ] = int(0)
        if direction in ["SL", "ED", "NR"]:
            goestointersection = intersection + 1
            if goestointersection % int(math.sqrt(intersections)) != 0:
                for trafficlightto in trafficlightlist:
                    direction = trafficlightto[0][1]
                    intersection = int(trafficlightto[0][3])
                    if intersection == goestointersection and direction == "E":
                        lightmatrix[
                            int(trafficlightfrom[1]), int(trafficlightto[1])
                        ] = int(0)
        if direction in ["WL", "SD", "ER"]:
            goestointersection = intersection + int(math.sqrt(intersections))
            if goestointersection < intersections:
                for trafficlightto in trafficlightlist:
                    direction = trafficlightto[0][1]
                    intersection = int(trafficlightto[0][3])
                    if intersection == goestointersection and direction == "S":
                        lightmatrix[
                            int(trafficlightfrom[1]), int(trafficlightto[1])
                        ] = int(0)
    return lightmatrix


def readroadmap():
    filepath = "Generatedmap.txt"
    roadmap = []
    spawns = []
    lights = []
    run = 0
    with open(filepath, "r") as roadmapfile:
        text = roadmapfile.readlines()
        header = text[0:4]
        cellsperlane = int(float(header[0].split("=")[1].strip()))
        gridsize = int(float(header[1].split("=")[1].strip()))
        streetlength = int(float(header[2].split("=")[1].strip()))
        intersections = int(float(header[3].split("=")[1].strip()))
        text = text[4:]
        height = len(text[0].split(","))
        numberoflights = 0
        for y, line in enumerate(text):
            road = line.strip().split(",")
            roadmap.append(road)
            for x, tile in enumerate(road):
                if tile.startswith("C"):
                    spawns.append([[x, y], tile])
                if tile.startswith("T"):
                    numberoflights += 1
                    lights.append([[x, y], tile])
                    run += 1
    return (
        roadmap,
        spawns,
        lights,
        height,
        cellsperlane,
        intersections,
        streetlength,
        gridsize,
    )


class Intersection(Model):
    '''
    Here the model is initialized
    a map file is read to place the lanes, traffic lights and spawn points
    '''
    def __init__(self):
        global NumberOfAgents
        self.schedule = RandomActivation(self)
        [
            self.roadmap,
            self.spawns,
            self.lights,
            self.height,
            self.cellsperlane,
            intersections,
            streetlength,
            gridsize,
        ] = readroadmap()
        self.width = self.height
        self.gridsize = gridsize
        self.streetlength = streetlength
        self.grid = MultiGrid(self.width, self.height, True)
        self.running = True
        self.tlightmatrix = np.empty((len(self.lights), len(self.lights)))
        self.tlightmatrix[:] = np.nan
        self.trafficlightlist = []
        self.carID = 0
        self.lightcombinations = [["SR", "SD", "SL", "WR"], ["ER", "ED", "EL", "SR"],
                                  ["NR", "ND", "NL", "ER"], ["WR", "WD", "WL", "NR"]]
        for i, light in enumerate(self.lights):
            direction = light[1][1]
            lane = light[1][2]
            location = light[0]
            xlocation = int(location[0])
            ylocation = self.height - 1 - int(location[1])
            trafficlight = TrafficLightAgent(
                f"{xlocation},{ylocation},{light[1][1:3]}", self, "red", direction, lane, i
            )
            self.trafficlightlist.append([light[1], i])
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))

        self.tlightmatrix = lightconnection(
            self.tlightmatrix, self.trafficlightlist, intersections
        )
        np.savetxt("data.csv", self.tlightmatrix, delimiter=",")

    def step(self):
        '''
        step function that will randomly place cars based on the spawn chance
        and will visit all the agents to perform their step function
        '''
        for spawn in self.spawns:
            if random.randint(0, 100) < SPAWNCHANCE:
                location = spawn[0]
                xlocation = int(location[0])
                ylocation = self.height - 1 - int(location[1])
                direction = spawn[1][1]
                lane = spawn[1][2]
                car = CarAgent(
                    f"car{self.carID}",
                    self,
                    50,
                    direction, lane,
                    [xlocation, ylocation],
                    self.streetlength,
                )
                self.carID += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (xlocation, ylocation))
        self.schedule.step()
