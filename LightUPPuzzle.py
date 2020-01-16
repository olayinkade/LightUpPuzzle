import sys;

# This function reads in the puzzle from the text file
def readpuzzle():
    txtfile = open('Puzzles.txt')
    print(txtfile.readline())
    dimension = txtfile.readline().split()
    row = int(dimension[0])


    puzzle = [[0 for x in range(row)] for y in range(row)]

    for x in range(row):
        for y in range(row+1):
            curr = txtfile.read(1)
            if curr != '\n':
                puzzle[x][y] = curr

    return puzzle
#This fuction is meant to validate the state of a puzzle give
# to see if it is valid
def puzzleValidation(puzzle):
    valid = True
    print(puzzle)

    return valid

def validBulbNextToAWall(puzzle):
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            if puzzle[x][y].isdigit():
                numOfBulbs = int(puzzle[x][y])
                validNeighbour = generateValidNeighbours(x, y, len(puzzle))
                seenbulbs= 0
                for z in range(len(validNeighbour)):
                    if puzzle[validNeighbour[z][0]][validNeighbour[z][1]] == "b":
                        seenbulbs += 1

                if numOfBulbs != seenbulbs:
                    return False
    return True

def validRowsAndCol(puzzle):
    for x in range(len(puzzle)):
        bulbSeen = False
        wallSeen = False
        for y in range(len(puzzle)):
            if bulbSeen and puzzle[y][x] == "b":
                return False
            elif wallSeen and puzzle[y][x] == "b":
                wallSeen = False
            elif puzzle[y][x] == "b":
                bulbSeen = True
            elif puzzle[y][x].isdigit():
                wallSeen = True

                # write column code

    return True








def generateValidNeighbours( row , col, length):
    validNeighbours = []
    if row > 0:
        validNeighbours.append([row - 1, col])
    if row < length-1:
        validNeighbours.append([row + 1, col])
    if col > 0:
        validNeighbours.append([row, col - 1])
    if col < length-1:
        validNeighbours.append([row, col + 1])

    return validNeighbours

print(puzzleValidation(readpuzzle()))