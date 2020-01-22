stack = []
variables = []

def priortize_variables(puzzle):
    invalid_neighbours = []
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            if puzzle[x][y].isdigit():
                valid_neighbours = generate_valid_neighbours(x, y, len(puzzle), puzzle)
                for z in range(len(valid_neighbours)):
                    for a in range(len(variables)):
                        if variables[a][1] == valid_neighbours[z]:
                            variables[a][0] += 1
                            break
            if puzzle[x][y] == '0':
                invalid_neighbours.extend(generate_valid_neighbours(x, y, len(puzzle), puzzle))

    for x in range(len(invalid_neighbours)):
        for y in range(len(variables)):
            if variables[y][1] == invalid_neighbours[x]:
                variables.remove(variables[y])
                break

    variables.sort()
    print(variables)


def backtrack():
    stack.append(([-1, -1], variables, 0, []))
    while True or stack != []:
        curr = stack.pop()
        if curr[0][0] != -1:
            puzzle = place_bulbs(curr[3], curr[0])
            is_valid_placement = valid_rows_and_cols(curr[0][1][0], curr[0][1][1], puzzle)
            reset(curr[3], curr[0])
            if is_valid_placement == False:
                continue

            curr[3].append(curr[0][1])
            #does validate the two constraints
        for x in range(len(curr[1])):
            child_position = curr[1][x]
            child_possible_values = list(curr[1])
            child_possible_values.remove(child_position)
            bulb_placed = []
            if curr[0][0] != -1:
                bulb_placed = curr[3]
            stack.append((child_position,  child_possible_values, curr[2]+1, bulb_placed))


def place_bulbs(existing_bulb, curr):
    puzzle = main_puzzle.copy()
    for x in range(len(existing_bulb)):
        puzzle[existing_bulb[x][0]][existing_bulb[x][1]] = 'b'

    puzzle[curr[1][0]][curr[1][1]] = "b"
    return puzzle


def reset(existing_bulb, curr):
    puzzle = main_puzzle.copy()
    for x in range(len(existing_bulb)):
        puzzle[existing_bulb[x][0]][existing_bulb[x][1]] = '_'

    puzzle[curr[1][0]][curr[1][1]] = "_"
    return puzzle




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
            if curr == "_":
                variables.append([0, [x, y]])

    print(variables)

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


def valid_rows_and_cols(row, col, puzzle):
    bulb_seen = False
    wall_seen = False

    bulb_seen_row = False
    wall_seen_row = False
    for y in range(len(puzzle)):
        if bulb_seen and puzzle[y][col] == "b":
            return False
        elif wall_seen and puzzle[y][col] == "b":
            wall_seen = False
            bulb_seen = True
        elif puzzle[y][col] == "b":
            bulb_seen = True
        elif bulb_seen and puzzle[y][col].isdigit():
            wall_seen = True
            bulb_seen = False

        if bulb_seen_row and puzzle[row][y] == "b":
            return False
        elif wall_seen_row and puzzle[row][y] == "b":
            wall_seen_row = False
            bulb_seen_row = True
        elif puzzle[row][y] == "b":
            bulb_seen_row = True
        elif bulb_seen_row and puzzle[row][y].isdigit():
            wall_seen_row = True
            bulb_seen_row = False

    return True


def generate_valid_neighbours(row, col, length, puzzle):
    valid_neighbours = []

    if row > 0:
        if puzzle[row - 1][col] == "_":
            valid_neighbours.append([row - 1, col])
    if row < length-1:
        if puzzle[row + 1][col] == "_":
            valid_neighbours.append([row + 1, col])
    if col > 0:
        if puzzle[row][col-1] == "_":
            valid_neighbours.append([row, col - 1])
    if col < length-1:
        if puzzle[row][col+1] == "_":
            valid_neighbours.append([row, col + 1])

    return valid_neighbours

# priortize_variables(read_puzzle())
# backtrack()
main_puzzle = read_puzzle()
print(main_puzzle)
priortize_variables(main_puzzle)
backtrack()