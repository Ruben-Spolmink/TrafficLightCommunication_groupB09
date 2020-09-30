from mesa import Agent, Model
import random

class TrafficLight(Agent):
    def __init__(self, name, model,trafficColor):
        super().__init__(name, model)
        self.trafficColor = "red"

    def step(self):
        if random.randint(0, 100) < 10:
            if self.trafficColor == "red":
                self.trafficColor = "green"
            else:
                self.trafficColor = "red"
