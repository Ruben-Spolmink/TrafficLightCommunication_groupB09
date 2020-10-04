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
        self.succes = True

    def move(self, direction, qmove):
        '''
        movement for a car based on the direction the car is moving
        in the case the move is a queue move a check is performed if the move was succesfull otherwise the move needs to be saved
        '''
        #self.speed=self.speed/3.6
        #self.speed=13.889
        unit=3*3.6
        #here I need to figure out how to measure distance between car and light
        #if car closer than 75m (25 squares) and the light is red and speed>0 acceleration-=5.646
        #if speed=0 and light=green and speed<50 acceleration+=6.775
        acceleration=0
        #move=int(self.speed/unit)
        move=1
        self.speed=self.speed-move+self.speed%unit+acceleration
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):

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
                    print("can't move")

    def move_queue(self):
        '''
        performing moves on basis of the queue. In the case that the move is not succesfull,
        because the car is blocked by an oter car the move will be placed back at the front of the queue
        '''
        templist = []
        if not (self.hasredlight()[0] and self.hasredlight()[1] == 0):
            current_move = self.queue.pop(0)
            self.qmove = True #now a q move is done instead of a normal move

            #if the car needs to move straight
            if current_move == "UP":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            #if the car needs to move left
            if current_move == "LEFT":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            #if the car needs to take a move right
            if current_move == "RIGHT":
                self.move(self.direction, self.qmove)
                if not (self.succes):
                    templist.append(current_move)
                    templist.extend(self.queue)
                    self.queue = templist
                    self.succes = True

            if not self.queue: #after the final move in the queue the new direciton and the new lane is set as the current direction and lane
                print("swapping lane and direction")
                self.lane = self.swaplane
                self.direction = self.turn

    def fill_queue(self):
        '''
        This function fills a queue with moves the car needs to take to cross the intersection and get in the correct lane.
        the turn left and right dicitonaries returns the correct direction the car is moving in after making the turn.
        The car is driving in a lane that either goes letf, rightthrough or right. At the intersection the car will randomly decide which direction it wants to move after the intersection.
        '''
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

        self.swaplane = random.choice(["L","D","R"]) #picks a random lane where the car will move in after the intersection

        #if the car is in the left lane set direction for a left turn
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

        #if the car is moving straight
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

        #if the car is in the right lane set the direciton to a right turn
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
        '''
        there are two situations for the cars either the car is driving or the car is at the intersection
        at the intersection a queue is filled with moves for a car and a new direcition is chosen.
        '''
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        if any(isinstance(agent, TrafficLightAgent) for agent in cell_contents): #a check if the car is at a traffic light or not
            if not self.queue:
                self.fill_queue()

        if not self.queue:
            self.qmove = False #wether the move is a normal move or a move from the queue
            self.move(self.direction,self.qmove)

        else:
            self.move_queue()
