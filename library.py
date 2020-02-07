from typing import List

stack = []
variables = []
invalid_wall = []
valid_wall = []


def read_puzzle():
    txt_file = open('Puzzles.txt')
    txt_file.readline()
    dimension = txt_file.readline().split()
    row = int(dimension[0])

    puzzle = [[0 for x in range(row)] for y in range(row)]

    for x in range(row):
        for y in range(row+1):
            curr = txt_file.read(1)
            if curr != '\n':
                puzzle[x][y] = curr
            if curr == "_":
                variables.append([0, [x, y]])
            if curr.isdigit():
                if curr == "0":
                    invalid_wall.append([x, y])
                else:
                    valid_wall.append([x, y])

    return puzzle


def generate_valid_neighbours(row, col, length, puzzle, bulb_inclusive=False):
    valid_neighbours = []

    if row > 0:
        if not puzzle[row-1][col].isdigit() and not (bulb_inclusive and (puzzle[row-1][col] == "b" or puzzle[row-1][col]
                                                                         == "*")):
            valid_neighbours.append([row - 1, col])
    if row < length-1:
        if not puzzle[row+1][col].isdigit() and not (bulb_inclusive and (puzzle[row+1][col] == "b" or puzzle[row+1][col]
                                                                         == "*")):
            valid_neighbours.append([row + 1, col])
    if col > 0:
        if not puzzle[row][col-1].isdigit() and not (bulb_inclusive and (puzzle[row][col-1] == "b" or puzzle[row][col-1]
                                                                         == "*")):
            valid_neighbours.append([row, col - 1])
    if col < length-1:
        if not puzzle[row][col+1].isdigit() and not (bulb_inclusive and (puzzle[row][col+1] == "b" or puzzle[row][col+1]
                                                                         == "*")):
            valid_neighbours.append([row, col + 1])

    return valid_neighbours


def print_puzzle(puzzle: List[List[str]]):
    print()
    for r in range(len(puzzle)):
        for c in range(len(puzzle[0])):
            print(puzzle[r][c], end=' ')
        print()
