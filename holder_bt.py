from makePuzzles import *
import copy
import time

wallNums = ['0', '1', '2', '3', '4']  # wall_values


def checkEdgeCorner(puz, i, j):
    # not an edge or corner status = 0
    # an edge, status = 1
    # a corner status = 2
    status = 0
    if (i == 0 or i == len(puz) - 1):
        status += 1
    if (j == 0 or j == len(puz[0]) - 1):
        status += 1

    return status


# count_walls_around
def countWalls(puz, i, j):
    # counts the number of walls adjacent to a cell
    # count increases 1 for walls 0-2.
    # Increases 2 for walls 3-4
    count = 0
    if i > 0 and puz[i - 1][j] in wallNums:
        count += int(int(puz[i - 1][j]) / 2 + 1)
    if i < len(puz) - 1 and puz[i + 1][j] in wallNums:
        count += int(int(puz[i + 1][j]) / 2) + 1
    if j > 0 and puz[i][j - 1] in wallNums:
        count += int(int(puz[i][j - 1]) / 2) + 1
    if j < len(puz[0]) - 1 and puz[i][j + 1] in wallNums:
        count += int(int(puz[i][j + 1]) / 2) + 1
    return count


# count_adjacent_lit_cells
def checkAdjBeams(puz, i, j):
    # counts the number of beams that are adjacent to the point
    count = 0
    if i > 0 and puz[i - 1][j] == '+':
        count += 1
    if i < len(puz) - 1 and puz[i + 1][j] == '+':
        count += 1
    if j > 0 and puz[i][j - 1] == '+':
        count += 1
    if j < len(puz[0]) - 1 and puz[i][j + 1] == '+':
        count += 1
    return count


# find_most_constraining
def findConstraining(puz, notassigned):
    rows = len(puz)
    cols = len(puz[0])
    winners = []
    maxCount = 0

    # marks the rays
    raytraceAll(puz)
    for val in notassigned:
        i = val[0]
        j = val[1]
        count = raytraceOne(puz, i, j)

        if count > maxCount:
            winners = [val]
            maxCount = count
        elif count == maxCount:
            winners.append(val)

    deRaytrace(puz)

    # print(winners)

    return winners[random.randint(0, len(winners) - 1)]


# find_most_constrained
def findConstrained(puz, notassigned):  # find_most_constrained
    rows = len(puz)
    cols = len(puz[0])
    winner = (-1, -1)

    # marks the rays
    raytraceAll(puz)

    # for each unassigned, check the contrained priority
    for val in notassigned:
        i = val[0]
        j = val[1]

        # check to see how many adjacent walls
        walls = countWalls(puz, i, j)
        # check to see if the cell is an edge, corner or neither
        loc = checkEdgeCorner(puz, i, j)
        # check to see how many beams are around the cell
        adjBeams = checkAdjBeams(puz, i, j)

        # add all these constraints up
        curr = walls + loc + adjBeams  # constraints

        # if the value is the same as the current leader, randomly pick which to keep
        if curr == winner[0] and random.randint(0, 1) == 0:
            winner = (curr, val)
        if curr > winner[0]:
            winner = (curr, val)

    deRaytrace(puz)

    return winner[1]


def getFromHeuristic(puz, notassigned, type):
    if type == 'random':
        index = random.randint(0, len(notassigned) - 1)
        ret = notassigned[index]
        notassigned.remove(ret)

    if type == 'constrained':
        ret = findConstrained(puz, notassigned)
        notassigned.remove(ret)

    if type == 'constraining':
        ret = findConstraining(puz, notassigned)
        notassigned.remove(ret)

    return ret


# print_puzzle
def printPuzzle(puz):
    rows = len(puz)
    cols = len(puz[0])
    for i in range(0, rows):
        for j in range(0, cols):
            print(puz[i][j], end=" ")
        print("\n")


# num_cells_should_be_lit
def raytraceOne(puz, i, j):
    rows = len(puz)
    cols = len(puz[0])
    count = 0
    # "raytrace" away from bulb, setting all _ to + in a line in every direction
    k = 1
    while i + k < rows and (puz[i + k][j] == "_" or puz[i + k][j] == "+"):
        if puz[i + k][j] == "_":
            count += 1
        k += 1
    k = 1
    while i - k >= 0 and (puz[i - k][j] == "_" or puz[i - k][j] == "+"):
        if puz[i - k][j] == "_":
            count += 1
        k += 1
    k = 1
    while j + k < cols and (puz[i][j + k] == "_" or puz[i][j + k] == "+"):
        if puz[i][j + k] == "_":
            count += 1
        k += 1
    k = 1
    while j - k >= 0 and (puz[i][j - k] == "_" or puz[i][j - k] == "+"):
        if puz[i][j - k] == "_":
            count += 1
        k += 1

    return count


# light_map_up
def raytraceAll(puz):
    rows = len(puz)
    cols = len(puz[0])
    for i in range(rows):
        for j in range(cols):
            # "raytrace" away from bulbs, setting all _ to + in a line in every direction
            if puz[i][j] == "b":
                k = 1
                while i + k < rows and (puz[i + k][j] == "_" or puz[i + k][j] == "+"):
                    puz[i + k][j] = "+"
                    k += 1
                k = 1
                while i - k >= 0 and (puz[i - k][j] == "_" or puz[i - k][j] == "+"):
                    puz[i - k][j] = "+"
                    k += 1
                k = 1
                while j + k < cols and (puz[i][j + k] == "_" or puz[i][j + k] == "+"):
                    puz[i][j + k] = "+"
                    k += 1
                k = 1
                while j - k >= 0 and (puz[i][j - k] == "_" or puz[i][j - k] == "+"):
                    puz[i][j - k] = "+"
                    k += 1
                k = 1


# is_map_lit_up_and_clean_map
def deRaytrace(puz):
    rows = len(puz)
    cols = len(puz[0])
    retVal = True
    for i in range(rows):
        for j in range(cols):
            if puz[i][j] == "_":
                retVal = False
            elif puz[i][j] == "+":
                puz[i][j] = "_"

    return retVal


# is_puzzle_solved
def complete(puz):
    global wallNums
    rows = len(puz)
    cols = len(puz[0])

    for i in range(rows):
        for j in range(cols):
            if puz[i][j] in wallNums and int(puz[i][j]) != numAdjacent(puz, i, j):
                return False

    raytraceAll(puz)

    if debug == "some":
        print("==== Check completeness")
        printPuzzle(puz)

    return deRaytrace(puz)


# count_adjacent_bulbs
def numAdjacent(puz, i, j):
    rows = len(puz)
    cols = len(puz[0])
    count = 0
    if i > 0 and puz[i - 1][j] == "b":
        count += 1
    if i < rows - 1 and puz[i + 1][j] == "b":
        count += 1
    if j > 0 and puz[i][j - 1] == "b":
        count += 1
    if j < cols - 1 and puz[i][j + 1] == "b":
        count += 1
    return count

# is_inside
def insidePuzzle(puz, i, j):
    rows = len(puz)
    cols = len(puz[0])
    return i >= 0 and j >= 0 and i < rows and j < cols


# can_bulb_be_here
def legal(puz, i, j):
    rows = len(puz)
    cols = len(puz[0])

    if debug == "some":
        print("==== Check legality")
        printPuzzle(puz)

    dx = (-1, 1, 0, 0)
    dy = (0, 0, -1, 1)
    for count in range(4):
        k = i + dx[count]
        l = j + dy[count]

        # check if we placed the bulb beside
        if insidePuzzle(puz, k, l) and puz[k][l] in wallNums:
            if numAdjacent(puz, k, l) > int(puz[k][l]):
                return False

        while insidePuzzle(puz, k, l) and not puz[k][l] in wallNums:
            if puz[k][l] == 'b':
                return False
            k += dx[count]
            l += dy[count]

    if debug == "some":
        print("Legal")
    return True


def getBlanks(puz):
    blanks = []
    for k in range(0, len(puz) * len(puz[0])):
        i = int(k / len(puz))
        j = int(k % len(puz[0]))
        if puz[i][j] == "_":
            blanks.append((i, j))
    return blanks


def solve(puz, heuristic):
    domain = ("b", "_")
    notassigned = getBlanks(puz)
    return backtrack(puz, domain, notassigned, heuristic)


countNodes = 0


def backtrack(puz, domain, notassigned, heuristic):
    if complete(puz):
        return puz

    global countNodes
    countNodes += 1
    if countNodes % 10000 == 0:
        print(countNodes, end='\r')

    if countNodes == 5000000:
        return 'timeout'

    if len(notassigned) == 0:
        return "back"

    val = getFromHeuristic(puz, notassigned, heuristic)
    i = val[0]
    j = val[1]

    for value in domain:
        puz[i][j] = value
        if (value != "_" and legal(puz, i, j)) or value == "_":
            result = backtrack(puz, domain, notassigned, heuristic)
            if result != "back":
                return result

    notassigned.append(val)
    return "back"


def clearSolution(puzzle):
    rows = len(puzzle)
    cols = len(puzzle[0])
    for i in range(rows):
        for j in range(cols):
            if puzzle[i][j] == 'b':
                puzzle[i][j] = '_'


def getTextInput(file):
    with open('input.txt') as f:
        puz = f.readlines()
    puz = [x.strip() for x in puz]
    puz.remove(puz[0])
    puz.remove(puz[0])

    for i in range(len(puz)):
        puz[i] = [x.strip() for x in puz[i]]

    return puz


debug = "none"


def main(argv=None):
    global debug

    if (argv == None):
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='create a modified Akari Puzzle')
    parser.add_argument('--width', action='store', dest='width', type=int, default=8)
    parser.add_argument('--height', action='store', dest='height', type=int, default=8)
    parser.add_argument('--verbose', '-v', action='count', dest='verbose', default=0)
    parser.add_argument('--count', '-c', action='store', dest='count', default=1)
    parser.add_argument('--solution', '-s', action='store_true', dest='solution', default=False)
    parser.add_argument('--bulbs', '-b', action='store', dest='bulbs', type=int, default=-1)
    parser.add_argument('--walls', '-w', action='store', dest='walls', type=int, default=-1)
    parser.add_argument('--debug', action='store', dest='debug', type=str, default="none")
    parser.add_argument('--heuristic', action='store', dest='heuristic', type=str, default="constrained")
    parser.add_argument('--input', action='store', dest='input', type=str, default="")

    args = parser.parse_args(argv)
    if (args.verbose > 0):
        print('AkariMaker {0}x{1} bulbs {2} walls {3}'.format(args.width, args.height, args.bulbs, args.walls))

    if args.input == '':
        puzzle = makePuzzles(args.count, args.width, args.height, args.bulbs, args.walls, args.solution)

        clearSolution(puzzle)

    else:
        puzzle = getTextInput(args.input)

    debug = args.debug
    print()

    start = time.time()
    solution = solve(puzzle, args.heuristic)
    end = time.time()

    if solution == 'timeout':
        print("Timeout!\nTime taken %f seconds" % (end - start))
    else:
        printPuzzle(solution)
        print("Time taken %f seconds\n" % (end - start))

    print("Nodes visited: %d\n" % (countNodes))


if __name__ == '__main__':
    main()
