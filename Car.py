from mesa import Agent, Model


class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, pos, lane, blok, route):
        super().__init__(name, model)
        self.speed = speed
        self.direction = direction
        self.pos = pos
        self.lane = lane
        self.blok = blok
        self.route = route

    def move(self):
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


    def step(self):
        #print("my position is " ,self.pos[0], self.pos[1])
        self.move()
