import math
import sys
import copy

"""
Generates the Generatedmap.txt file that contains the layout of the road and intersections.
Call as follows: roadmapgenerator.py gridsize streetlength intersections
Gridsize is the size of a cell in cm. e.g. 10 means the cells are 10x10 cm
Streetlength is the length of a street between intersections in cm
Intersections is the number of intersections (must be the square of a number)
The streets leading to the intersections from the edges are 1/2*streetlength
We assume here that the street is 3m wide.
Outer street lengths are 1/2 * streetlength, the distance between intersections is streetlength
"""


def generatepattern(streetlength, gridsize):
    # Generates the pattern for the roadmap, this pattern is later copied into multiple directions.
    pattern = []
    cellsperlane = 300 / gridsize
    cellsperstreet = streetlength / gridsize / 2
    if not cellsperlane.is_integer():
        cellsperlane = int(cellsperlane)
        print("300/gridsize is no integer, cellsperlane is now %d " % cellsperlane)
    if not cellsperstreet.is_integer():
        cellsperstreet = int(cellsperstreet)
        print(
            "streetlength/gridsize/2 is no integer, cellsperlane is now %d "
            % cellsperstreet
        )
    cellsperlane = int(cellsperlane)
    cellsperstreet = int(cellsperstreet)
    # Upper part of the intersection
    for i in range(cellsperstreet - 1):
        row = []
        for j in range(cellsperstreet):
            row.append("X,")
        for j in range(cellsperlane):
            row.append("SR,")
        for j in range(cellsperlane):
            row.append("SD,")
        for j in range(cellsperlane):
            row.append("SL,")
        for j in range(cellsperlane):
            row.append("NL,")
        for j in range(cellsperlane):
            row.append("ND,")
        for j in range(cellsperlane):
            row.append("NR,")
        for j in range(cellsperstreet):
            row.append("X,")
        pattern.append(row)
    lastrow = []
    for j in range(cellsperstreet):
        lastrow.append("X,")
    for j in range(cellsperlane):
        lastrow.append("TSR0,")
    for j in range(cellsperlane):
        lastrow.append("TSD0,")
    for j in range(cellsperlane):
        lastrow.append("TSL0,")
    for j in range(cellsperlane):
        lastrow.append("NL,")
    for j in range(cellsperlane):
        lastrow.append("ND,")
    for j in range(cellsperlane):
        lastrow.append("NR,")
    for j in range(cellsperstreet):
        lastrow.append("X,")
    pattern.append(lastrow)
    # Middle part of the intersection
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WR,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        row.append("TWR0,")
        for j in range(cellsperstreet - 1):
            row.append("WR,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WD,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        row.append("TWD0,")
        for j in range(cellsperstreet - 1):
            row.append("WD,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WL,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        row.append("TWL0,")
        for j in range(cellsperstreet - 1):
            row.append("WL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet - 1):
            row.append("EL,")
        row.append("TEL0,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("EL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet - 1):
            row.append("ED,")
        row.append("TED0,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("ED,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet - 1):
            row.append("ER,")
        row.append("TER0,")
        for j in range(6 * cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("ER,")
        pattern.append(row)
    # Lower part of the intersection
    firstrow = []
    for j in range(cellsperstreet):
        firstrow.append("X,")
    for j in range(cellsperlane):
        firstrow.append("SR,")
    for j in range(cellsperlane):
        firstrow.append("SD,")
    for j in range(cellsperlane):
        firstrow.append("SL,")
    for j in range(cellsperlane):
        firstrow.append("TNL0,")
    for j in range(cellsperlane):
        firstrow.append("TND0,")
    for j in range(cellsperlane):
        firstrow.append("TNR0,")
    for j in range(cellsperstreet):
        firstrow.append("X,")
    pattern.append(firstrow)
    for i in range(cellsperstreet - 1):
        row = []
        for j in range(cellsperstreet):
            row.append("X,")
        for j in range(cellsperlane):
            row.append("SR,")
        for j in range(cellsperlane):
            row.append("SD,")
        for j in range(cellsperlane):
            row.append("SL,")
        for j in range(cellsperlane):
            row.append("NL,")
        for j in range(cellsperlane):
            row.append("ND,")
        for j in range(cellsperlane):
            row.append("NR,")
        for j in range(cellsperstreet):
            row.append("X,")
        pattern.append(row)
    return pattern, len(pattern), len(pattern[0])


def generatemap(gridsize, streetlength, intersections):
    if not math.sqrt(intersections).is_integer():
        print("Intersections should be the square of an integer")
        exit()
    if not (streetlength / gridsize).is_integer():
        print("streetlength/gridzise should be an integer")
        exit()
    # grass = "X"
    # road for going north, east, south, west = N,E,S,W
    # lane for going right, straight, left = R,D,L
    # car spawns = C
    # intersection numbers = 0
    [pattern, height, width] = generatepattern(streetlength, gridsize)
    print("Pattern created")
    # Expand rows
    for j, row in enumerate(pattern):
        ogrow = copy.deepcopy(row)
        for i in range(int(math.sqrt(intersections)) - 1):
            for k, element in enumerate(ogrow):
                if "0" in element:
                    ogrow[k] = element[:-2] + f"{i+1},"
            pattern[j].extend(ogrow)
    print("Rows extended")
    # Expand columns
    ogpattern = copy.deepcopy(pattern)
    for i in range(int(math.sqrt(intersections)) - 1):
        for row in ogpattern:
            rowcopy = copy.deepcopy(row)
            for k, element in enumerate(rowcopy):
                if any(map(str.isdigit, element)):
                    intnumber = element[-2]
                    rowcopy[k] = (
                        element[:-2]
                        + f"{int(intnumber)+int(math.sqrt(intersections))},"
                    )
            pattern.append(rowcopy)
    print("Rows added")
    # Remove last 's
    for i in range(len(pattern)):
        pattern[i][-1] = pattern[i][-1].split(",")[0]
    return pattern


def createspawns(map, gridsize, streetlength, intersections):
    # Creates the car spawns on the sides of the outer intersections
    for i in range(int(math.sqrt(intersections))):
        row = i * len(map[1]) / math.sqrt(intersections)
        # row = last grass patch
        row = row + streetlength / 2 / gridsize - 1
        # First half row
        row = row + math.ceil(300 / gridsize / 2)
        for i in range(3):
            map[int(row)][-1] = "C" + map[int(row)][-1]
            map[0][int(row)] = "C" + map[0][int(row)]
            row = row + 300 / gridsize
        for i in range(3):
            map[int(row)][0] = "C" + map[int(row)][0]
            map[-1][int(row)] = "C" + map[-1][int(row)]
            row = row + 300 / gridsize

    return map


def createheader(map, gridsize, streetlength, intersections):
    # Creates a header that contains creation information, useful for initializing the model.
    cellsperlane = 300 / gridsize
    map.insert(0, f"cellsperlane = {cellsperlane}")
    map.insert(1, f"gridsize = {gridsize}")
    map.insert(2, f"streetlength = {streetlength}")
    map.insert(3, f"intersections = {intersections}")
    return map


if len(sys.argv) == 4:
    gridsize = int(sys.argv[1])
    streetlength = int(sys.argv[2])
    intersections = int(sys.argv[3])
else:
    gridsize = 10
    streetlength = 30000
    intersections = 1
map = generatemap(gridsize, streetlength, intersections)
map = createspawns(map, gridsize, streetlength, intersections)
map = createheader(map, gridsize, streetlength, intersections)
with open("Generatedmap.txt", "w") as mapfile:
    for row in map:
        for element in row:
            mapfile.write(str(element))
        mapfile.write("\n")
