from model import Intersection
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import sys
from mesa.visualization.UserParam import UserSettableParameter
from mesa.batchrunner import BatchRunner

#uncomment if there are windows issues
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

co2 = ["CO2",  "#00AA00"]
nox = ["NOx", "#880000"]
pm = ["PM10", "#000000"]

tactics = ["Standard", "Proportional"] # , "Offset" , "Lookahead", "GreenWave"
cycletime = [30]# 60, 90

settings = {
    "offset": UserSettableParameter("choice", value=1, choices=[0, 1, 2, 3], description="Set offset for offset tactic"),
    "tactic": UserSettableParameter(
    "choice", value="Standard", choices=tactics, description="Tactics that the traffic lights use"
            ),
    "cycletime": UserSettableParameter("slider", "Cycletime", 60, 0, 100, 1, description="Choose the amount of time"
                                                                                         "that a traffic light is green"
                                                                                         ""),
    "spawnrate": UserSettableParameter(
        "slider",
        "Spawnrate",
        5,
        0,
        20,
        1,
        description="Choose how many agents to include in the model",
        )
    }

variableParams = {"tactic": tactics,
                  "spawnrate": [2, 5],
                  "cycletime": [30]
                  }
#, 10
# 60, 90
fixedparams = {"offset": 0}
modelreporters = {"CO2": lambda m: Intersection.getco2,
                  "NOx": lambda m: Intersection.getnox,
                  "PM10": lambda m: Intersection.getpm,
                  "AverageTraveltime": lambda m: Intersection.getaveragetraveltime,
                  "AverageEmission": lambda m: Intersection.getaverageemission}

CO2chart = ChartModule([{"Label": co2[0], "Color": co2[1]}])
NOXchart = ChartModule([{"Label": nox[0], "Color": nox[1]}])
pmchart = ChartModule([{"Label": pm[0], "Color": pm[1]}])

# Default runs with visualization
if len(sys.argv) == 1:
    spawnrate = settings["spawnrate"]
    tactic = settings["tactic"]
    offset = settings["offset"]
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic, offset, cycletime).width, Intersection(spawnrate, tactic, offset, cycletime).height, 700, 700
    )
    server = ModularServer(Intersection, [grid, CO2chart, NOXchart, pmchart], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
elif sys.argv[1] == "Batch":
    batch = BatchRunner(Intersection, variable_parameters=variableParams, fixed_parameters=fixedparams,
                        iterations=2, max_steps=1000, model_reporters=modelreporters)
    batch.run_all()
    data = batch.get_model_vars_dataframe()
    print(data)
elif sys.argv[1] == "Headless":
    spawnrate = int(sys.argv[2])
    tactic = str(sys.argv[3])
    intersectionmodel = Intersection(spawnrate, tactic)
    for i in range(1000):
        intersectionmodel.step()
