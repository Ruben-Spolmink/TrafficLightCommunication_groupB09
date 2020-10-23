from Legend import *
import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
import math
from Car import CarAgent
from TrafficLight import TrafficLightAgent
from mesa.datacollection import DataCollector


def reademissionvalues():
    emissionvalues = {}
    with open("emission.txt") as emissionfile:
        lines = emissionfile.readlines()
        lines.pop(0)
        for line in lines:
            [cat, values] = line.split(":")
            values = [float(x) for x in (values.split(","))]
            emissionvalues[cat] = values
    return emissionvalues


def lightconnection(lightmatrix, trafficlightlist, intersections):
    # Creates a np array where all 0's are connections between traffic lights (what traffic light sends car to
    # what trafic light).
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
    # Reads the generatedmap.txt and converts it into a list of lists, which can be used to locate traffic lights
    # and car spawns.
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
                if tile.startswith("C"):  # C indicates car spawn
                    spawns.append([[x, y], tile])
                if tile.startswith("T"):  # T indicates traffic light
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
    """
    Here the model is initialized. The Generatedmap.txt is read in order to locate traffic lights and car spawns.
    Cars and traffic lights are spawned here.
    """

    def __init__(self, spawnrate=10, tactic="Standard"):
        self.tactic = tactic  # [Standard, Offset, Proportional, Lookahead, GreenWave]
        self.spawnrate = spawnrate
        self.offset = 3
        self.spawnnumber = 4
        self.schedule = RandomActivation(self)
        self.slowmotionrate = 0.1
        self.emissionvalues = reademissionvalues()
        [
            self.roadmap,
            self.spawns,
            self.lights,
            self.height,
            self.cellsperlane,
            self.intersections,
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
        self.lightcombinations = [
            ["SR", "SD", "SL", "WR"],
            ["ER", "ED", "EL", "SR"],
            ["NR", "ND", "NL", "ER"],
            ["WR", "WD", "WL", "NR"],
        ]
        # Needed for green wave
        self.mostcars = []
        self.goesto = []
        self.cycletime = 60
        self.firstgreenintersection = -1
        self.secondgreenintersection = -1
        self.firstcombination = None
        self.secondcombination = None
        self.firstcycledone = 0

        # Needed for lookahead
        self.mostexpectedcars = [0, 0, 0]

        self.intersectionmatrix = []  # matrix with intersectionnumbers in the right index
        lastnumber = 0
        for i in range(int(math.sqrt(self.intersections))):
            tempmaptrix = []
            for j in range(int(math.sqrt(self.intersections))):
                tempmaptrix.append(j + lastnumber)
            lastnumber = tempmaptrix[-1] + 1
            self.intersectionmatrix.append(tempmaptrix)
        self.intersectionmatrix = np.array(self.intersectionmatrix)

        # Data collection
        # self.dc = DataCollector(
        #     model_reporters={"agent_count": lambdam: m.schedule.get_agent_count()}, agent_reporters = {
        #     "name": lambdaa: a.name})

        # Initialize information dictionary
        self.trafficlightinfo = {}
        for i in range(self.intersections):
            self.trafficlightinfo.update({f"intersection{i}": {"Trafficlightinfo": {},
                                                               "Timeinfo": {}}})

        for i, light in enumerate(self.lights):  # Initializes traffic lights
            self.trafficlightinfo[f"intersection{light[1][3]}"]["Trafficlightinfo"][f"{light[1][1:3]}"] = i
            self.trafficlightinfo[f"intersection{light[1][3]}"]["Timeinfo"].update({"Currentgreen": -1,
                                                                                      "Currenttimegreen": 0,
                                                                                      "Maxtimegreen": 0,
                                                                                      "Allred": 1})
            intersectionnumber = int(light[1][3])
            intersectiony = np.where(self.intersectionmatrix == intersectionnumber)[0]
            intersectionx = np.where(self.intersectionmatrix == intersectionnumber)[1]
            direction = light[1][1]
            lane = light[1][2]
            location = light[0]
            xlocation = int(location[0])
            ylocation = self.height - 1 - int(location[1])
            trafficlight = TrafficLightAgent(
                f"{xlocation},{ylocation},{light[1][1:3]}",
                self,
                "red",
                direction,
                lane,
                i,
                intersectionnumber,
                self.tactic,
                self.offset,
                [intersectionx, intersectiony],
                self.cycletime,
            )
            self.trafficlightlist.append([light[1], i])
            self.schedule.add(trafficlight)
            self.grid.place_agent(trafficlight, (xlocation, ylocation))
        self.tlightmatrix = lightconnection(
            self.tlightmatrix, self.trafficlightlist, self.intersections
        )

        # Place legend
        self.grid.place_agent(LegendCarIcon("Caricon", self), (65, 68))
        self.grid.place_agent(LegendGreenTlightIcon("GreenTlighticon", self), (65, 69))
        self.grid.place_agent(LegendRedTlightIcon("RedTlighticon", self), (65, 70))

    def step(self):
        """
        Step function that will randomly place cars based on the spawn chance
        and will visit all the agents to perform their step function.
        """
        # Determine intersection of most cars and where they go to
        if self.tactic == "GreenWave" and\
                len(self.schedule.agents) > 12 * self.intersections and\
                ((self.schedule.steps % (self.cycletime * 2)) == 0):

            self.firstcycledone = 0
            self.mostcars = np.argmax(np.nansum(self.tlightmatrix, axis=1))
            self.goesto = np.where(~np.isnan(self.tlightmatrix[self.mostcars]))
            self.firstgreenintersection = self.lights[self.mostcars][1][3]
            self.secondgreenintersection = self.lights[self.goesto[0][0]][1][3]

            # Determines the direction of traffic lights
            firstdirection = self.schedule.agents[int(self.mostcars)].direction
            seconddirection = self.schedule.agents[self.goesto[0][0]].direction

            # Determines combinations of traffic lights that can stay green
            for i, combination in enumerate(self.lightcombinations):
                if firstdirection + "D" in combination:
                    self.firstcombination = self.lightcombinations[i]
                if seconddirection + "D" in combination:
                    self.secondcombination = self.lightcombinations[i]
            # If 1st part of green wave is over (so 1 cycle has been done)
            if not ((self.schedule.steps % (self.cycletime * 2)) == 0):
                self.firstcycledone = 1

        if self.tactic == "Proportional" and len(self.schedule.agents) > 12 * self.intersections:
            for i in range(self.intersections):
                currenttimegreen = self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"]
                maxgreentime = self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Maxtimegreen"]
                self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"] = currenttimegreen + 1
                if currenttimegreen > maxgreentime + 6:
                    carsinfront = np.nansum(self.tlightmatrix, axis=1)
                    totalcars = [0, 0, 0, 0]
                    for key in self.trafficlightinfo[f"intersection{i}"]["Trafficlightinfo"].keys():
                        trafficlight = int(self.trafficlightinfo[f"intersection{i}"]["Trafficlightinfo"][key])
                        cars = carsinfront[trafficlight]
                        for j, combi in enumerate(self.lightcombinations):
                            if key in combi:
                                totalcars[j] = totalcars[j] + cars
                    # No cars? pick regular timeschedule
                    if sum(totalcars) == 0:
                        totalcars = [1, 1, 1, 1]
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currentgreen"] = \
                        totalcars.index(max(totalcars))
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Maxtimegreen"] = \
                       max(totalcars)/(sum(totalcars)/4)*self.cycletime
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"] = 0
                if currenttimegreen == maxgreentime:
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currentgreen"] = -1

        if self.tactic == "Lookahead" and len(self.schedule.agents) > 12 * self.intersections:
            self.mostexpectedcars = [0, 0, 0] # cars,intersection,combination
            for i in range(self.intersections):
                currenttimegreen = self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"]
                maxgreentime = self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Maxtimegreen"]
                self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"] = currenttimegreen + 1
                if currenttimegreen > maxgreentime + 6:
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Allred"] = 0
                    carsexpected = np.nansum(self.tlightmatrix, axis=0)
                    carsinfront = np.nansum(self.tlightmatrix, axis=1)
                    totalcars = [0, 0, 0, 0]
                    # For every direction + lane in intersection
                    for key in self.trafficlightinfo[f"intersection{i}"]["Trafficlightinfo"].keys():
                        trafficlight = int(self.trafficlightinfo[f"intersection{i}"]["Trafficlightinfo"][key])
                        cars = carsinfront[trafficlight]
                        # For every lightcombination
                        for j, combi in enumerate(self.lightcombinations):
                            if key in combi:
                                totalcars[j] = totalcars[j] + cars + carsexpected[trafficlight]
                                if totalcars[j] > self.mostexpectedcars[0]:
                                    self.mostexpectedcars[0] = totalcars[j]
                                    self.mostexpectedcars[1] = i
                                    self.mostexpectedcars[2] = j
                    # Reset timers
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currentgreen"] = \
                        (self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currentgreen"] + 1) % 4
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Maxtimegreen"] = \
                       self.cycletime
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Currenttimegreen"] = 0
                if currenttimegreen == maxgreentime:
                    self.trafficlightinfo[f"intersection{i}"]["Timeinfo"]["Allred"] = 1
            if self.mostexpectedcars[0] != 0:
                # Change green light information of intersection with most expected cars
                self.trafficlightinfo[f"intersection{self.mostexpectedcars[1]}"]["Timeinfo"]["Currentgreen"] =\
                    self.mostexpectedcars[2]

                # Get trafficlightnumbers of ligths where most cars are expected
                mostcars = 0
                mostcarslight = None
                comingfrom = np.nansum(self.tlightmatrix, axis=1)
                for direction in self.lightcombinations[self.mostexpectedcars[2]]:
                    greenlight = int(self.trafficlightinfo[f"intersection{self.mostexpectedcars[1]}"]\
                                                        ["Trafficlightinfo"][direction])
                    # Where the cars to those lights come from.
                    lightscomingfrom = np.argwhere(~np.isnan(self.tlightmatrix[:, greenlight]))
                    for light in lightscomingfrom:
                        if light:
                            light = light[0]
                            carsinfront = np.sum(comingfrom[light])
                            if carsinfront > mostcars:
                                mostcars = int(carsinfront)
                                mostcarslight = light

                # Find intersection + directon of this light and change this intersection's green light information
                if mostcars != 0:
                    intersection = int(self.lights[mostcarslight][1][3])
                    direction = self.lights[mostcarslight][1][1:3]
                    for k, directs in enumerate(self.lightcombinations):
                        if direction in directs[0:3]:
                            self.trafficlightinfo[f"intersection{intersection}"]["Timeinfo"]["Currentgreen"] = k
                            pass


        for spawn in self.spawns:
            location = spawn[0]
            cell_contents = self.grid.get_cell_list_contents([location])
            if not cell_contents and random.randint(0, 100/self.slowmotionrate) < self.spawnrate:
                location = spawn[0]
                xlocation = int(location[0])
                ylocation = self.height - 1 - int(location[1])
                direction = spawn[1][1]
                lane = spawn[1][2]
                car = CarAgent(
                f"car{self.carID}", self, 50, direction, lane, [xlocation, ylocation], self.streetlength)
                self.carID += 1
                self.schedule.add(car)
                self.grid.place_agent(car, (xlocation, ylocation))

        self.schedule.step()
