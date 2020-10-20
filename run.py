from model import Intersection
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import sys
from mesa.visualization.UserParam import UserSettableParameter

#uncomment if there are windows issues
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

settings = {"tactic": "Standard",
            "spawnrate": UserSettableParameter(
                "slider",
                "Spawnrate",
                30,
                0,
                50,
                1,
                description="Choose how many agents to include in the model",
            )
            }


# Default runs with visualization
if len(sys.argv) == 1:
    spawnrate = settings["spawnrate"]
    tactic = settings["tactic"]
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic).width, Intersection(spawnrate, tactic).height, 1000, 1000
    )
    server = ModularServer(Intersection, [grid], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
elif sys.argv[1] == "Batch":
    pass
    # batchrun
elif sys.argv[1] == "Headless":
    spawnrate = int(sys.argv[2])
    tactic = str(sys.argv[3])
    intersectionmodel = Intersection(spawnrate, tactic)
    while 1:
        intersectionmodel.step()
elif sys.argv[1] == "Visualize":
    spawnrate = int(sys.argv[2])
    tactic = str(sys.argv[3])
    settings["spawnrate"] = spawnrate
    settings["tactic"] = tactic
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic).width, Intersection(spawnrate, tactic).height, 1000, 1000
    )
    server = ModularServer(Intersection, [grid], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
