import sys


# This function reads in the puzzle from the text file
def read_puzzle():
    txt_file = open('Puzzles.txt')
    print(txt_file.readline())
    dimension = txt_file.readline().split()
    row = int(dimension[0])

    puzzle = [[0 for x in range(row)] for y in range(row)]

    for x in range(row):
        for y in range(row+1):
            curr = txt_file.read(1)
            if curr != '\n':
                puzzle[x][y] = curr

    return puzzle


# This function is meant to validate the state of a puzzle give
# to see if it is valid
def puzzle_validation(puzzle):
    valid = True
    # print(puzzle)

    return valid


def valid_bulb_next_to_wall(puzzle):
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            if puzzle[x][y].isdigit():
                num_of_bulbs = int(puzzle[x][y])
                valid_neighbour = generate_valid_neighbours(x, y, len(puzzle))
                seen_bulbs= 0
                for z in range(len(valid_neighbour)):
                    if puzzle[valid_neighbour[z][0]][valid_neighbour[z][1]] == "b":
                        seen_bulbs += 1
                if num_of_bulbs != seen_bulbs:
                    return False
    return True


def valid_rows_and_cols(puzzle):
    for x in range(len(puzzle)):
        bulb_seen = False
        wall_seen = False
        for y in range(len(puzzle)):
            if bulb_seen and puzzle[y][x] == "b":
                return False
            elif wall_seen and puzzle[y][x] == "b":
                wall_seen = False
            elif puzzle[y][x] == "b":
                bulb_seen = True
            elif puzzle[y][x].isdigit():
                wall_seen = True

            # write column code

    return True


def generate_valid_neighbours(row, col, length):

    valid_neighbours = []
    if row > 0:
        valid_neighbours.append([row - 1, col])
    if row < length-1:
        valid_neighbours.append([row + 1, col])
    if col > 0:
        valid_neighbours.append([row, col - 1])
    if col < length-1:
        valid_neighbours.append([row, col + 1])

    return valid_neighbours

# print(puzzlevalidation(readpuzzle()))