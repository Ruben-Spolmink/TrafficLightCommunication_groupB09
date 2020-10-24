from model import Intersection
from Portrayal import agent_portrayal
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import sys
from mesa.visualization.UserParam import UserSettableParameter

#uncomment if there are windows issues
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

co2 = ["CO2",  "#00AA00"]
nox = ["NOx", "#880000"]
pm =  ["PM10", "#000000"]

print("Hello welcome to traffic")
print("We have two options either (1)headless for running the simulation and get the data or (2)visualization to be see the model and interact")
userInput = input("1 for headless \n2 for visualization : ")
userInt = int(userInput)
if(userInt == 1):
    print("you chose headless")
    userSpawn = int(input("Please enter the spawnrate : "))
    print("There are 3 tactics to choose from: \n(1)bla bla, (2)bla bla, (3)bla bla")
    userTactic = input("Please enter the tactic you want to use for the traffic lights : ")
    userTick = int(input("Please enter the number of steps the model has to perform : "))
    userBatch = int(input("Please enter the amount of batches you want to run : "))

elif(userInt == 2):
    print("you chose visualization")


settings = {"tactic": "Standard",
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

CO2chart = ChartModule([{"Label" : co2[0], "Color": co2[1]}])
# Default runs with visualization
"""
if userInt == 1:
    spawnrate = settings["spawnrate"]
    tactic = settings["tactic"]
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic).width, Intersection(spawnrate, tactic).height, 1000, 1000
    )
    server = ModularServer(Intersection, [grid, CO2chart], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
"""
"""
elif sys.argv[1] == "Batch":
    pass
    # batchrun
"""
if userInt == 1:
    spawnrate = userSpawn
    tactic = userTactic
    for i in range(userBatch):
        intersectionmodel = Intersection(spawnrate, tactic)
        for j in range(userTick):
            intersectionmodel.step()

if userInt == 2:
    spawnrate = 10
    tactic = "Proportional"
    settings["spawnrate"] = spawnrate
    settings["tactic"] = tactic
    grid = CanvasGrid(
        agent_portrayal, Intersection(spawnrate, tactic).width, Intersection(spawnrate, tactic).height, 1000, 1000
    )
    #server = ModularServer(Intersection, [grid], "Intersectionmodel", settings)
    server = ModularServer(Intersection, [grid, CO2chart], "Intersectionmodel", settings)
    server.port = 8520  # The default
    server.launch()
