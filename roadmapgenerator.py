import math
import sys
import copy

# Generate roadmap
# Call as follows: roadmapgenerator.py gridsize, streetlength, intersections
# gridsize is the size of a cell in cm. e.g. 10 means the cells are 10x10 cm
# streetlength is the length of a street between intersections in cm
# intersections is the number of intersections (must be the square of a number)
# The streets leading to the intersections from the edges are 1/2*streetlength
def generatepattern(streetlength, gridsize):
    # assuming street = 3m wide
    # Outer street lengths are 1/2 * streetlength, distance between intersections is streetlength
    pattern = []
    cellsperlane = 300/gridsize
    cellsperstreet = streetlength/gridsize/2
    if not cellsperlane.is_integer():
        cellsperlane = int(cellsperlane)
        print("300/gridsize is no integer, cellsperlane is now %d " % cellsperlane)
    if not cellsperstreet.is_integer():
        cellsperstreet = int(cellsperstreet)
        print("streetlength/gridsize/2 is no integer, cellsperlane is now %d " % cellsperstreet)
    cellsperlane = int(cellsperlane)
    cellsperstreet = int(cellsperstreet)
    # Upper part
    for i in range(cellsperstreet-1):
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
        lastrow.append("TSR,")
    for j in range(cellsperlane):
        lastrow.append("TSD,")
    for j in range(cellsperlane):
        lastrow.append("TSL,")
    for j in range(cellsperlane):
        lastrow.append("TNL,")
    for j in range(cellsperlane):
        lastrow.append("TND,")
    for j in range(cellsperlane):
        lastrow.append("TNR,")
    for j in range(cellsperstreet):
        lastrow.append("X,")
    pattern.append(lastrow)
    # Middle part
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("WR,")
        row.append("TWR,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TWR,")
        for j in range(cellsperstreet-1):
            row.append("WR,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("WD,")
        row.append("TWD,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TWD,")
        for j in range(cellsperstreet-1):
            row.append("WD,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("WL,")
        row.append("TWL,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TWL,")
        for j in range(cellsperstreet-1):
            row.append("WL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("EL,")
        row.append("TEL,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TEL,")
        for j in range(cellsperstreet-1):
            row.append("EL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("ED,")
        row.append("TED,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TED,")
        for j in range(cellsperstreet-1):
            row.append("ED,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet-1):
            row.append("ER,")
        row.append("TER,")
        for j in range(6*cellsperlane):
            row.append("O,")
        row.append("TER,")
        for j in range(cellsperstreet-1):
            row.append("ER,")
        pattern.append(row)
    # Lower part
    firstrow = []
    for j in range(cellsperstreet):
        firstrow.append("X,")
    for j in range(cellsperlane):
        firstrow.append("TSR,")
    for j in range(cellsperlane):
        firstrow.append("TSD,")
    for j in range(cellsperlane):
        firstrow.append("TSL,")
    for j in range(cellsperlane):
        firstrow.append("TNL,")
    for j in range(cellsperlane):
        firstrow.append("TND,")
    for j in range(cellsperlane):
        firstrow.append("TNR,")
    for j in range(cellsperstreet):
        firstrow.append("X,")
    pattern.append(firstrow)
    for i in range(cellsperstreet-1):
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
    if not (streetlength/gridsize).is_integer():
        print("streetlength/gridzise should be an integer")
        exit()
    # grass = "x"
    # road for going north, east, south, west = n, e, s, w
    # lane for going right, straight, left = r, d, l
    [pattern, height, width] = generatepattern(streetlength, gridsize)
    print("Pattern created")
    # Expand rows
    for j, row in enumerate(pattern):
        ogrow = row
        for i in range(int(math.sqrt(intersections))-1):
            pattern[j].extend(ogrow)
    print("Rows extended")
    # Expand columns
    ogpattern = copy.deepcopy(pattern)
    for i in range(int(math.sqrt(intersections))-1):
        for row in ogpattern:
            pattern.append(row)
    print("Rows added")
    # Remove last 's
    for i in range(len(pattern)):
        pattern[i][-1] = pattern[i][-1].split(',')[0]
    return pattern


if len(sys.argv) == 4:
    gridsize = int(sys.argv[1])
    streetlength = int(sys.argv[2])
    intersections = int(sys.argv[3])
else:
    gridsize = 10
    streetlength = 30000
    intersections = 1
map = generatemap(gridsize, streetlength, intersections)
with open("Generatedmap.txt", "w") as mapfile:
    for row in map:
        for element in row:
            mapfile.write(str(element))
        mapfile.write("\n")
