from mesa import Agent


class LegendCarIcon(Agent):
    """ Class for creating the car legend icon"""

    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "CarIcon"
        self.model = intersectionmodel


class LegendTlightIcon(Agent):
    """ Class for creating the traffic light legend icon"""

    def __init__(self, name, intersectionmodel):
        super().__init__(name, intersectionmodel)
        self.name = "TlightIcon"
        self.model = intersectionmodel
