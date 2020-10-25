from model import Intersection
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import sys
from mesa.visualization.UserParam import UserSettableParameter
from mesa.batchrunner import BatchRunner
import pandas as pd
from model import batchrun

#uncomment if there are windows issues
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

co2 = ["CO2",  "#00AA00"]
nox = ["NOx", "#880000"]
pm = ["PM10", "#000000"]

tactics = ["Standard", "Proportional", "Offset" , "Lookahead", "GreenWave"]

settings = {
    "offset": UserSettableParameter("choice", "Offset", value=1, choices=[0, 1, 2, 3], description="Set offset for offset tactic"),
    "tactic": UserSettableParameter(
    "choice","Tactic", value="Standard", choices=tactics, description="Tactics that the traffic lights use"
            ),
    "cycletime": UserSettableParameter("slider", "Cycletime", 60, 0, 120, 1, description="Choose the amount of time"
                                                                                         "that a traffic light is green"
                                                                                         ""),
    "spawnrate": UserSettableParameter(
        "slider",
        "Spawnrate",
        5,
        0,
        10,
        1,
        description="Choose how many agents to include in the model",
        )
    }

variableParams = {"tactic": tactics,
                  "spawnrate": [5],
                  "cycletime": [30]
                  }

fixedparams = {"offset": 0}

CO2chart = ChartModule([{"Label": co2[0], "Color": co2[1]}])
NOXchart = ChartModule([{"Label": nox[0], "Color": nox[1]}])
pmchart = ChartModule([{"Label": pm[0], "Color": pm[1]}])

# Default runs with visualization
if len(sys.argv) == 1:
    spawnrate = settings["spawnrate"]
    tactic = settings["tactic"]
    offset = settings["offset"]
    cycletime = settings["cycletime"]
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic, offset, cycletime).width, Intersection(spawnrate, tactic, offset, cycletime).height, 700, 700
    )
    server = ModularServer(Intersection, [grid, CO2chart, NOXchart, pmchart], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
elif sys.argv[1] == "Batch":
    batchrun()
elif sys.argv[1] == "Headless":
    offset = settings["offset"]
    spawnrate = int(sys.argv[2])
    tactic = str(sys.argv[3])
    intersectionmodel = Intersection(spawnrate, tactic, offset)
    for i in range(1000):
        intersectionmodel.step()
