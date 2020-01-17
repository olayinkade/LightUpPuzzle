import sys


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
def puzzlevalidation(puzzle):
    valid = True
    # print(puzzle)

    return valid


def validbulbnexttowall(puzzle):
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            if puzzle[x][y].isdigit():
                numofbulbs = int(puzzle[x][y])
                validNeighbour = generatevalidneighbours(x, y, len(puzzle))
                seenbulbs= 0
                for z in range(len(validNeighbour)):
                    if puzzle[validNeighbour[z][0]][validNeighbour[z][1]] == "b":
                        seenbulbs += 1
                if numofbulbs != seenbulbs:
                    return False
    return True


def validrowsandcol(puzzle):
    for x in range(len(puzzle)):
        bulbseen = False
        wallseen = False
        for y in range(len(puzzle)):
            if bulbseen and puzzle[y][x] == "b":
                return False
            elif wallseen and puzzle[y][x] == "b":
                wallseen = False
            elif puzzle[y][x] == "b":
                bulbseen = True
            elif puzzle[y][x].isdigit():
                wallseen = True

            # write column code

    return True



def generatevalidneighbours(row,col,length):

    validneighbours = []
    if row > 0:
        validneighbours.append([row - 1, col])
    if row < length-1:
        validneighbours.append([row + 1, col])
    if col > 0:
        validneighbours.append([row, col - 1])
    if col < length-1:
        validneighbours.append([row, col + 1])

    return validneighbours

# print(puzzlevalidation(readpuzzle()))