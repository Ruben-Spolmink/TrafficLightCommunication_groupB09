from mesa import Agent, Model

class TrafficLight(Agent):
    def __init__(self, name, model,trafficColor):
        super().__init__(name, model)
        self.trafficColor = ""

    def step(self):
        pass
