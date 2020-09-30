from mesa import Agent, Model
import TrafficLight
import Model


class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, pos, blok, route, streetlength):
        super().__init__(name, model)
        self.speed = speed
        self.model = model
        self.direction = direction
        self.pos = pos
        self.blok = blok
        self.route = route

    def move(self):
        if not self.hasredlight()[0]:
            if(self.direction == "N"):
                new_position = (self.pos[0], self.pos[1]+1)
            if(self.direction == "E"):
                new_position = (self.pos[0]+1, self.pos[1])
            if(self.direction == "S"):
                new_position = (self.pos[0], self.pos[1]-1)
            if(self.direction == "W"):
                new_position = (self.pos[0]-1, self.pos[1])
            if self.model.grid.out_of_bounds((new_position[0], new_position[1])):
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                cell_contents = self.model.grid.get_cell_list_contents([new_position])#gets a list of agents in that cell
                if not any(isinstance(agent, CarAgent) for agent in cell_contents): #complex statement that checks if there aren't any cars in that cell
                    self.model.grid.move_agent(self, new_position)#all clear move to cell

    def hasredlight(self):
        distance = 0
        hasredlight = False
        color = " "
        if self.direction == "E":
            for i in range(int(self.model.streetlength/self.model.gridsize)-1):
                if not self.model.grid.out_of_bounds((self.pos[0] + i, self.pos[1])):
                    gridcoordinates = (self.pos[0] + i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLight.TrafficLight):
                            color = agent.trafficColor
                            distance = i
                            print(f"trafficcolor:{color}")
                            break
        if self.direction == "W":
            for i in range(int(self.model.streetlength/self.model.gridsize)-1):
                if not self.model.grid.out_of_bounds((self.pos[0] - i, self.pos[1])):
                    gridcoordinates = (self.pos[0] - i, self.pos[1])
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLight.TrafficLight):
                            color = agent.trafficColor
                            distance = i
                            print(f"trafficcolor:{color}")
                            break
        if self.direction == "N":
            for i in range(int(self.model.streetlength/self.model.gridsize)-1):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + i)):
                    gridcoordinates = (self.pos[0], self.pos[1] + i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLight.TrafficLight):
                            color = agent.trafficColor
                            distance = i
                            print(f"trafficcolor:{color}")
                            break
        if self.direction == "S":
            for i in range(int(self.model.streetlength/self.model.gridsize) -1):
                if not self.model.grid.out_of_bounds((self.pos[0], self.pos[1] - i)):
                    gridcoordinates = (self.pos[0], self.pos[1] - i)
                    agents = self.model.grid.get_cell_list_contents(gridcoordinates)
                    for agent in agents:
                        if isinstance(agent, TrafficLight.TrafficLight):
                            color = agent.trafficColor
                            distance = i
                            break
        if color == "red":
            hasredlight = True
        return hasredlight, distance


    def step(self):
        #print("my position is " ,self.pos[0], self.pos[1])
        self.move()
