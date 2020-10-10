from mesa import Agent
import numpy as np


class TrafficLightAgent(Agent):
    """Class for traffic lights. The cars in front are calculated and the messageboard is updated"""

    def __init__(self, name, intersectionmodel, trafficColor, direction, lane, number, intersectionnumber, tactic,
                 offset, intersectionindex, cycletime):
        super().__init__(name, intersectionmodel)
        self.offset = offset
        self.intersectionnumber = intersectionnumber
        self.model = intersectionmodel
        self.id = number
        self.lane = lane
        self.trafficColor = trafficColor
        self.direction = direction
        self.cycletime = cycletime
        self.tactic = tactic
        self.intersectionx = intersectionindex[0]
        self.intersectiony = intersectionindex[1]

    def step(self):
        carcount = self.carsinfront()
        self.model.tlightmatrix[self.id, :][
            self.model.tlightmatrix[self.id, :] >= 0
        ] = (carcount / 3)
        time = self.model.schedule.time
        if self.tactic == "Standard" or self.tactic == "Offset":
            self.changecoloroffset(time, self.direction, self.lane, self.cycletime)
        elif self.tactic == "Lookahead":
            pass
        elif self.tactic == "GreenWave":
            self.changecolorgreenwave(time, self.direction, self.lane, self.cycletime)
        else :
            print("Tactic not specified")
            assert()

    def carsinfront(self):
        """Calculates the number of cars in front of the traffic light."""
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
        return infront - 1  # traffic light counts itself

    def changecoloroffset(self, time, direction, lane, cycletime):
        """Changes color of the traffic lights"""
        combi = direction + lane
        timeperiod = time % (cycletime * 4)
        self.trafficColor = "red"
        if self.intersectiony % 2 == self.intersectionx % 2:
            offset = self.offset
        else:
            offset = 0
        if (
            6 <= timeperiod <= cycletime - 1
            and combi in self.model.lightcombinations[(0 + offset) % 4]
        ):
            self.trafficColor = "green"
        if (
            cycletime + 6 <= timeperiod <= cycletime * 2 - 1
            and combi in self.model.lightcombinations[(1 + offset) % 4]
        ):
            self.trafficColor = "green"
        if (
            cycletime * 2 + 6 <= timeperiod <= cycletime * 3 - 1
            and combi in self.model.lightcombinations[(2 + offset) % 4]
        ):
            self.trafficColor = "green"
        if (
            cycletime * 3 + 6 <= timeperiod <= cycletime * 4 - 1
            and combi in self.model.lightcombinations[(3 + offset) % 4]
        ):
            self.trafficColor = "green"

    def changecolorgreenwave(self, time, direction, lane, cycletime):
        """Changes color of the traffic lights"""

        combi = direction + lane
        timeperiod = time % (cycletime * 4)
        self.trafficColor = "red"

        # If not part of green wave or first cycle is done do usual stuff
        if (int(self.intersectionnumber) != int(self.model.firstgreenintersection) or self.model.firstcycledone) and \
            int(self.intersectionnumber) != int(self.model.secondgreenintersection):
            if self.intersectiony % 2 == self.intersectionx % 2:
                offset = self.offset
            else:
                offset = 0
            if (
                6 <= timeperiod <= cycletime - 1
                and combi in self.model.lightcombinations[(0 + offset) % 4]
            ):
                self.trafficColor = "green"
            if (
                cycletime + 6 <= timeperiod <= cycletime * 2 - 1
                and combi in self.model.lightcombinations[(1 + offset) % 4]
            ):
                self.trafficColor = "green"
            if (
                cycletime * 2 + 6 <= timeperiod <= cycletime * 3 - 1
                and combi in self.model.lightcombinations[(2 + offset) % 4]
            ):
                self.trafficColor = "green"
            if (
                cycletime * 3 + 6 <= timeperiod <= cycletime * 4 - 1
                and combi in self.model.lightcombinations[(3 + offset) % 4]
            ):
                self.trafficColor = "green"
        # Else turn green if part of the right combi of lights
        else:
            if combi in self.model.firstcombination and \
                    int(self.intersectionnumber) == int(self.model.firstgreenintersection) and\
                    timeperiod % cycletime > 5:
                self.trafficColor = "green"
            if combi in self.model.secondcombination and \
                    int(self.intersectionnumber) == int(self.model.secondgreenintersection):
                if self.model.firstcycledone:
                    self.trafficColor = "green"
                elif timeperiod % cycletime > 5:
                    self.trafficColor = "green"




