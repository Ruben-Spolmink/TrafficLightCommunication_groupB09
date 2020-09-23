from mesa import Agent, Model

class TrafficLight(Agent):
    def __init__(self, name, model,trafficColor):
        super().__init__(name, model)
        self.trafficColor = "red"

    def step(self):
        if(self.trafficColor == "red"):
            self.trafficColor = "green"
        else:
            self.trafficColor = "red"
