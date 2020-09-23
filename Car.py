from mesa import Agent, Model

class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, pos):
        super().__init__(name, model)
        self.speed = speed
        self.direction = direction
        self.pos = pos

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center = False)
        if(self.direction == "n"):
            new_position = (self.pos[0]+1, self.pos[1])
        if(self.direction == "e"):
            new_position = (self.pos[0], self.pos[1]-1)
        if(self.direction == "s"):
            new_position = (self.pos[0]-1, self.pos[1])
        if(self.direction == "w"):
            new_position = (self.pos[0], self.pos[1]+1)

        if new_position in possible_steps:#checks if new position is not out of the grid
            cell_contents = self.model.grid.get_cell_list_contents([new_position])#gets a list of agents in that cell
            if not any(isinstance(agent, CarAgent) for agent in cell_contents): #complex statement that checks if there aren't any cars in that cell
                self.model.grid.move_agent(self, new_position)#all clear move to cell

    def step(self):
        #print("my position is " ,self.pos[0], self.pos[1])
        self.move()
