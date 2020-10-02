from mesa import Agent, Model
import model
from TrafficLight import TrafficLightAgent
import random

class CarAgent(Agent):
    def __init__(
        self, name, intersectionmodel, speed, direction, lane, pos, streetlength
    ):
        super().__init__(name, intersectionmodel)
        self.model = intersectionmodel
        self.speed = speed
        self.direction = direction
        self.pos = pos
        self.queue = []
        self.lane = lane
        self.swaplane = ""
        self.turn = ""
        self.qmove = False

    def move(self, direction, qmove):
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):

            if direction == "N":
                new_position = (self.pos[0], self.pos[1] + 1)
            if direction == "E":
                new_position = (self.pos[0] + 1, self.pos[1])
            if direction == "S":
                new_position = (self.pos[0], self.pos[1] - 1)
            if direction == "W":
                new_position = (self.pos[0] - 1, self.pos[1])
            if self.model.grid.out_of_bounds((new_position[0], new_position[1])):
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                cell_contents = self.model.grid.get_cell_list_contents(
                    [new_position]
                )  # gets a list of agents in that cell
                if not any(
                    isinstance(agent, CarAgent) for agent in cell_contents
                ):  # complex statement that checks if there aren't any cars in that cell
                    self.model.grid.move_agent(
                        self, new_position
                    )  # all clear move to cell
                elif(qmove == True):
                    return False


    def move_queue(self):
        templist = []
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):
            current_move = self.queue.pop(0)
            self.qmove = True
            if current_move == "UP":
                if not(self.move(self.direction, self.qmove)) :
                    templist.append(current_move)
                    templist.append(self.queue)
                    self.queue = templist
            if current_move == "LEFT":
                if not(self.move(self.direction, self.qmove)) :
                    templist.append(current_move)
                    templist.append(self.queue)
                    self.queue = templist
            if current_move == "RIGHT":
                if not(self.move(self.direction, self.qmove)) :
                    templist.append(current_move)
                    templist.append(self.queue)
                    self.queue = templist
            if self.queue == []:
                self.lane = self.swaplane
                self.direction = self.turn

    def fill_queue(self):
        turn_left = {
                    "N": "W",
                    "E": "N",
                    "S": "E",
                    "W": "S"}

        turn_right = {
                    "N": "E",
                    "E": "S",
                    "S": "W",
                    "W": "N"}

        self.swaplane = random.choice(["L","D","R"])
        if self.lane == "L":
            self.turn = turn_left[self.direction]
            if self.swaplane == "L":
                for i in range(4):
                    self.queue.append("UP")
            if self.swaplane == "D":
                for i in range(5):
                    self.queue.append("UP")
            if self.swaplane == "R":
                for i in range(6):
                    self.queue.append("UP")
        if self.lane == "D":
            self.turn = self.direction
            if self.swaplane == "L":
                for i in range(7):
                    self.queue.append("UP")
                self.queue.append("LEFT")
            if self.swaplane == "D":
                for i in range(7):
                    self.queue.append("UP")
            if self.swaplane == "R":
                for i in range(7):
                    self.queue.append("UP")
        if self.lane == "R":
            self.turn = turn_right[self.direction]
            if self.swaplane == "L":
                for i in range(3):
                    self.queue.append("UP")
            if self.swaplane == "D":
                for i in range(2):
                    self.queue.append("UP")
            if self.swaplane == "R":
                self.queue.append("UP")

    def hasredlight(self):
        distance = 1
        hasredlight = False
        color = "green"
        if self.direction == "E":
            for i in range(int(self.model.streetlength / self.model.gridsize) - 1):
                if not self.model.grid.out_of_bounds((self.pos[0] + i, self.pos[1])):
                    gridcoordinates = (self.pos[0] + i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLightAgent):
                            color = agent.trafficColor
                            distance = i
                            break
        if self.direction == "W":
            for i in range(int(self.model.streetlength / self.model.gridsize) - 1):
                if not self.model.grid.out_of_bounds((self.pos[0] - i, self.pos[1])):
                    gridcoordinates = (self.pos[0] - i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLightAgent):
                            color = agent.trafficColor
                            distance = i
                            break
        if self.direction == "N":
            for i in range(int(self.model.streetlength / self.model.gridsize) - 1):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + i)):
                    gridcoordinates = (self.pos[0], self.pos[1] + i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLightAgent):
                            color = agent.trafficColor
                            distance = i
                            break
        if self.direction == "S":
            for i in range(int(self.model.streetlength / self.model.gridsize) - 1):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] - i)):
                    gridcoordinates = (self.pos[0], self.pos[1] - i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLightAgent):
                            color = agent.trafficColor
                            distance = i
                            break
        if color == "red":
            hasredlight = True
        return hasredlight, distance

    def step(self):
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        if any(isinstance(agent, TrafficLightAgent) for agent in cell_contents):
            self.fill_queue()
        if not self.queue:
            self.qmove = False
            self.move(self.direction,self.qmove)
        else:
            self.move_queue()
