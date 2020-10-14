from mesa import Agent, Model

class RoadSegment(Agent):
    def __init__(self, name, model, direction, trafficColor):
        super().__init__(name, model)
        self.direction = direction
        self.trafficColor = " "

    def step(self):
        pass
