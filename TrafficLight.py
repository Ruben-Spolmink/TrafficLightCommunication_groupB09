from mesa import Agent, Model
import random
import numpy as np


class TrafficLightAgent(Agent):
    def __init__(self, name, intersectionmodel, trafficColor, direction, number):
        super().__init__(name, intersectionmodel)
        self.model = intersectionmodel
        self.id = number
        self.trafficColor = trafficColor
        self.direction = direction

    def step(self):
        carcount = self.carsinfront()
        self.model.tlightmatrix[self.id, :][self.model.tlightmatrix[self.id, :] >= 0] = carcount/3
        print(self.model.tlightmatrix)
        if random.randint(0, 100) < 10:
            if self.trafficColor == "red":
                self.trafficColor = "green"
            else:
                self.trafficColor = "red"

    def carsinfront(self):
        infront = 0
        if self.direction == "N":
            for i in range(int(self.model.streetlength / self.model.gridsize)):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] - i)):
                    gridcoordinates = (self.pos[0], self.pos[1] - i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    infront = infront + len(agents)

        if self.direction == "E":
            for i in range(int(self.model.streetlength / self.model.gridsize)):
                if not self.model.grid.out_of_bounds((self.pos[0] - i, self.pos[1])):
                    gridcoordinates = (self.pos[0] - i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    infront = infront + len(agents)
        if self.direction == "S":
            for i in range(int(self.model.streetlength / self.model.gridsize)):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + i)):
                    gridcoordinates = (self.pos[0], self.pos[1] + i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    infront = infront + len(agents)
        if self.direction == "W":
            for i in range(int(self.model.streetlength / self.model.gridsize)):
                if not self.model.grid.out_of_bounds((self.pos[0] + i, self.pos[1])):
                    gridcoordinates = (self.pos[0] + i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    infront = infront + len(agents)
        np.set_printoptions(threshold=np.inf)
        return infront - 1 # traffic light counts itself
