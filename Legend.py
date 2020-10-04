from mesa import Agent
from model import *


class LegendCarIcon(Agent):
    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "CarIcon"
        self.model = intersectionmodel

class LegendCarText(Agent):
    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "CarText"
        self.model = intersectionmodel

class LegendTlightIcon(Agent):
    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "TlightIcon"
        self.model = intersectionmodel

class LegendTlightText(Agent):
    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "TlightText"
        self.model = intersectionmodel