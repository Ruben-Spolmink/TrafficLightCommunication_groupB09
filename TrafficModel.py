from mesa import Agent, Model

class TrafficModel(Model):
    def __init__(self, N, M)
    self.num_Cars = N
    self.num_TrafficLights = M

    def step(self):
        self.schedule.step()
