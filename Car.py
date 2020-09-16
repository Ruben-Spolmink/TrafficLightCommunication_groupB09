from mesa import Agent, Model

class Car(Agent):
    def __init__(self, unique_id):
        super().__init__(unique_id, model)
    def step(self):
        #what actions to do
