import math
import sys
import copy


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
    for i in range(cellsperstreet):
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
    # Middle part
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WR,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("WR,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WD,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("WD,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("WL,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("WL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("EL,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("EL,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("ED,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("ED,")
        pattern.append(row)
    for i in range(cellsperlane):
        row = []
        for j in range(cellsperstreet):
            row.append("ER,")
        for j in range(6*cellsperlane):
            row.append("O,")
        for j in range(cellsperstreet):
            row.append("ER,")
        pattern.append(row)
    # Lower part
    for i in range(cellsperstreet):
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
        mapfile.write(str(row) + "\n")
