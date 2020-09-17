from mesa import Agent, Model

class CarAgent(Agent):
    def __init__(self, name, model, speed, direction, goal, nextlane):
        super().__init__(name, model)
        self.speed = speed
        self.direction = direction
        self.goal = ""
        self.nextlane = ""

    def step(self):
        pass
