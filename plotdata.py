import pandas as pd
import matplotlib.pyplot as plt

dflook = pd.read_csv("./Data/Lookahead.csv")
dfgreen = pd.read_csv("./Data/GreenWave.csv")
dfoff = pd.read_csv("./Data/Offset.csv")

dfworse1 = pd.read_csv("./Data/Offsetworse.csv")
dfworse5 = pd.read_csv("./Data/Offsetworse5.csv")
dfworse6 = pd.read_csv("./Data/Offsetworse6.csv")
dfworse7 = pd.read_csv("./Data/Offsetworse7.csv")
dfworse8 = pd.read_csv("./Data/Offsetworse8.csv")
dfworse9 = pd.read_csv("./Data/Offsetworse9.csv")
dfworse10 = pd.read_csv("./Data/Offsetworse10.csv")

dfworse = pd.concat([dfworse1, dfworse5, dfworse6,dfworse7,dfworse8,dfworse9,dfworse10])

dfgreen.rename(columns={'Unnamed: 0':'Iteration'}, inplace=True)
dflook.rename(columns={'Unnamed: 0':'Iteration'}, inplace=True)
dfoff.rename(columns={'Unnamed: 0':'Iteration'}, inplace=True)
dfworse.rename(columns={'Unnamed: 0':'Iteration'}, inplace=True)

dfgreen["AverageTraveltime"] = dfgreen["AverageTraveltime"].div(5)
dflook["AverageTraveltime"] = dflook["AverageTraveltime"].div(5)
dfoff["AverageTraveltime"] = dfoff["AverageTraveltime"].div(5)
dfworse["AverageTraveltime"] = dfworse["AverageTraveltime"].div(5)

lastrowslook = dflook.loc[dflook["Iteration"] % 50000 == 49999]
lastrowsgreen = dfgreen.loc[dfgreen["Iteration"] % 50000 == 49999]
lastrowsoff = dfoff.loc[dfoff["Iteration"] % 50000 == 49999]
lastrowsworse = dfworse.loc[dfworse["Iteration"] % 50000 == 49999]
index = ["Offset = 0", "Greenwave", "Lookahead", "Offset = 2"]

spawnrates = [1, 2, 3, 4, 5]
s1mean = []
s2mean = []
s3mean = []
s4mean = []
s5mean = []
s1std = []
s2std = []
s3std = []
s4std = []
s5std = []

for spawnrate in spawnrates:
    spawngreen = lastrowsgreen.loc[lastrowsgreen["Spawnrate"] == spawnrate]
    spawnlook = lastrowslook.loc[lastrowslook["Spawnrate"] == spawnrate]
    spawnoff = lastrowsoff.loc[lastrowsoff["Spawnrate"] == spawnrate]
    spawnworse = lastrowsworse.loc[lastrowsworse["Spawnrate"] == spawnrate]

    meangreen = spawngreen.mean()["AveragePM"]
    stdevgreen = spawngreen.std()["AveragePM"]
    meanlook = spawnlook.mean()["AveragePM"]
    stdevlook = spawnlook.std()["AveragePM"]
    meanoff = spawnoff.mean()["AveragePM"]
    stdevoff = spawnoff.std()["AveragePM"]
    meanworse = spawnworse.mean()["AveragePM"]
    stdevworse = spawnworse.std()["AveragePM"]
    if spawnrate == 1:
        s1mean = [meanoff, meangreen, meanlook, meanworse]
        s1std = [stdevoff, stdevgreen, stdevlook, stdevworse]
    if spawnrate == 2:
        s2mean = [meanoff, meangreen, meanlook, meanworse]
        s2std = [stdevoff, stdevgreen, stdevlook, stdevworse]
    if spawnrate == 3:
        s3mean = [meanoff, meangreen, meanlook, meanworse]
        s3std = [stdevoff, stdevgreen, stdevlook, stdevworse]
    if spawnrate == 4:
        s4mean = [meanoff, meangreen, meanlook, meanworse]
        s4std = [stdevoff, stdevgreen, stdevlook, stdevworse]
    if spawnrate == 5:
        s5mean = [meanoff, meangreen, meanlook, meanworse]
        s5std = [stdevoff, stdevgreen, stdevlook, stdevworse]

df = pd.DataFrame({"Spawnrate 1": s1mean,
                   "Spawnrate 2": s2mean,
                   "Spawnrate 3": s3mean,
                   "Spawnrate 4": s4mean,
                   "Spawnarate 5": s5mean}, index=index)
errors = pd.DataFrame({"1": s1std,
                       "2": s2std,
                       "3": s3std,
                       "4": s4std,
                       "5": s5std})
ax = df.plot(kind="bar", yerr=errors[["1", "2", "3", "4", "5"]].values.T, title="Average $PM_{10}$ emission")
ax.set_xlabel("Strategies")
ax.set_ylabel("Average $PM_{10}$ emission per car [g]")
# pd.concat([df, errors]).to_csv("./Data/AverageTraveltime.csv")
plt.show()

