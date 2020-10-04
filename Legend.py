from mesa import Agent


class LegendCarIcon(Agent):
    """ Class for creating the car legend icon"""

    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "CarIcon"
        self.model = intersectionmodel


class LegendGreenTlightIcon(Agent):
    """ Class for creating the green traffic light legend icon"""

    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "greenTlightIcon"
        self.model = intersectionmodel


class LegendRedTlightIcon(Agent):
    """ Class for creating the red traffic light legend icon"""

    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "redTlightIcon"
        self.model = intersectionmodel
