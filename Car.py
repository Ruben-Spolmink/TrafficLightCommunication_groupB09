from mesa import Agent, Model

class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, pos):
        super().__init__(name, model)
        self.speed = speed
        self.direction = direction
        self.pos = pos

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center = False)
        print(self.direction)
        if(self.direction == "n"):
            new_position = (self.pos[0]+1, self.pos[1])
        if(self.direction == "e"):
            new_position = (self.pos[0], self.pos[1]-1)
        if(self.direction == "s"):
            new_position = (self.pos[0]-1, self.pos[1])
        if(self.direction == "w"):
            new_position = (self.pos[0], self.pos[1]+1)

        if new_position in possible_steps:
            self.model.grid.move_agent(self, new_position)

    def step(self):
        print("my position is " ,self.pos[0], self.pos[1])
        self.move()
