import csv

from mesa import Agent, Model
import model
from TrafficLight import TrafficLightAgent
import random


class CarAgent(Agent):
    """Class for cars, movement and vision of cars are handled here."""

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
        self.succes = True

    def move(self, direction, qmove):
        """
        The movement of the car is handled here, guided by the direction of the car.
         When a car passes a trafficlight, moves get queued up.
         In the case the move is a queued move, a check is performed.
         If the move couldn't be performed, it's saved again.
        """
        # IN PROGRESS



        # self.speed=self.speed/3.6
        # self.speed=13.889
        unit = 3 * 3.6 * 3
        # here I need to figure out how to measure distance between car and light
        # if car closer than 75m (25 squares) and the light is red and speed>0 acceleration=-5.646
        # if speed<50 and light=green and speed<50 acceleration=6.775
        acceleration = 0
        move=int(self.speed/unit)
        #move = 1
        self.speed = self.speed - move + self.speed % unit + acceleration

        #temporary solution - just stop dead when we hit a red light - can also be permanent solution if we dont care abt deceleration
        if self.hasredlight()[0] and self.hasredlight()[1] == 0:
            self.speed=0;

        #chek if speed outside parameters
        if self.speed>50:
            self.speed=50;
            acceleration=0;

        if self.speed<0:
             self.speed=0;
             acceleration=0;
        # Checks whether the car can move and what it's new position is going to be.
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):
            #acceleration from stop, we might want to make this parameter of speed to model non-monotonous acceleration
            if self.speed<50:
                acceleration=6.775

            if direction == "N":
                new_position = (self.pos[0], self.pos[1] + move)
            if direction == "E":
                new_position = (self.pos[0] + move, self.pos[1])
            if direction == "S":
                new_position = (self.pos[0], self.pos[1] - move)
            if direction == "W":
                new_position = (self.pos[0] - move, self.pos[1])
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
                    self.succes = True
                elif qmove:
                    self.succes = False

    def move_queue(self):
        """
        Performing moves on basis of the queue. In the case that the move is not succesfull,
        because the car is blocked by an oter car the move will be placed back at the front of the queue
        """
        templist = []
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):
            current_move = self.queue.pop(0)
            self.qmove = True  # now a q move is done instead of a normal move

            # if the car needs to move straight
            if current_move == "UP":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            # if the car needs to move left
            if current_move == "LEFT":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            # if the car needs to take a move right
            if current_move == "RIGHT":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            if (
                not self.queue
            ):  # after the final move in the queue the new direciton and the new lane is set as the current direction and lane
                self.lane = self.swaplane
                self.direction = self.turn

    def fill_queue(self):
        """
        This function fills a queue with moves the car needs to take to cross the intersection and get in the correct
        lane. The turn left and right dicitonaries returns the correct direction the car is moving in after making
        the turn. The car is driving in a lane that either goes letf, rightthrough or right. At the intersection
        the car will randomly decide which direction it wants to move after the intersection.
        """
        turn_left = {"N": "W", "E": "N", "S": "E", "W": "S"}

        turn_right = {"N": "E", "E": "S", "S": "W", "W": "N"}

        self.swaplane = random.choice(
            ["L", "D", "R"]
        )  # Picks a random lane where the car will move in.

        # If the car is in the left lane set direction for a left turn
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

        # If the car is moving straight
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

        # If the car is in the right lane set the direciton to a right turn
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
        """
        The car determines whether it has red light or not and outputs a boolean (true if red light, false if not).
        It also returns the distance to the traffic light.
        """
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
        """
        There are two situations for the cars either the car is driving or the car is at the intersection
        at the intersection a queue is filled with moves for a car and a new direction is chosen.
        """
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        # A check if the car is at a traffic light or not
        if any(isinstance(agent, TrafficLightAgent) for agent in cell_contents):
            if not self.queue:
                self.fill_queue()

        if not self.queue:
            self.qmove = False  # Check whether the move is one from the queue or a standard move.
            self.move(self.direction, self.qmove)

        else:
            self.move_queue()

    # def emission(self, speed, acceleration):
    #     """
    #     IN PROGRESS
    #
    #     ToDo: add import CSV; add an acceleration to the cars; implement function fully
    #
    #     This function outputs a cars emissions based on the speed and acceleration and stores them in a table.
    #     The emissions are both measured in absolute mg/s as well as porportional to their overall emission shares.
    #     """
    #     emissionData = open("emission.txt") # load the emission data file
    #
    #     with open('emission.csv', mode='w') as emission_file:
    #         emission_writer = csv.writer(emission_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #         emission_writer.writerow(['John Smith', 'Accounting', 'November'])
    #         emission_writer.writerow(['Erica Meyers', 'IT', 'March'])
    #
    #     for i in range(self): # for every car, evaluate the emission data and store it in the emission.csv file
    #
    #         # Velocity (0-30, 30-60), Acceleration (+ 0.5, 0.5-1.2, 1.2+  m/s2), CO, HC, NOx, absolute, proportional
    #         if self.speed < 30:
    #             if self.acceleration < 0.5:
    #                 emissionData[]
    #                 pass
    #             elif self.acceleration > 0.5 & self.acceleration < 1.2:
    #
    #                 pass
    #             elif self.acceleration > 1.2:
    #
    #                 pass
    #             pass
    #         if self.speed >= 30:
    #             if self.acceleration < 0.5:
    #                 emissionData[]
    #                 pass
    #             elif self.acceleration > 0.5 & self.acceleration < 1.2:
    #
    #                 pass
    #             elif self.acceleration > 1.2:
    #
    #                 pass
    #             pass
    #     pass
