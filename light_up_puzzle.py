import random
stack = []
variables = []
invalid_wall = []
valid_wall = []


def prioritize_variables(puzzle):
    invalid_neighbours = []
    for x in range(len(valid_wall)):
        valid_neighbours = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
        for z in range(len(valid_neighbours)):
            for a in range(len(variables)):
                if variables[a][1] == valid_neighbours[z]:
                    variables[a][0] += 1
                    break
    for x in range(len(invalid_wall)):
        invalid_neighbours.extend(generate_valid_neighbours(invalid_wall[x][0],
                                                            invalid_wall[x][1], len(puzzle), puzzle))

    for x in range(len(invalid_neighbours)):
        for y in range(len(variables)):
            if variables[y][1] == invalid_neighbours[x]:
                variables.remove(variables[y])
                break

    for x in range(len(valid_wall)):
        value = puzzle[valid_wall[x][0]][valid_wall[x][1]]
        sure_variable = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
        if int(value) == len(sure_variable):
            for y in range(len(sure_variable)):
                for z in range(len(variables)):
                    if variables[z][1] == sure_variable[y]:
                        variables[z][0] = 6

    variables.sort()


def backtrack():
    stack.append(([-1, -1], variables, 0, []))
    global num_nodes
    num_nodes = 1
    while stack != []:
        curr = stack.pop()
        num_nodes += 1
        if curr[0][0] != -1:
            puzzle = place_bulbs(curr[3], curr[0][1], "b", "_", "*")
            is_valid_row_col = valid_rows_and_cols(curr[0][1][0], curr[0][1][1], puzzle)

            if not is_valid_row_col:
                place_bulbs(curr[3], curr[0][1], "_", "*", "_")
                continue
            is_valid_bulb_around_wall = validate_bulbs_next_to_wall(puzzle)
            if not is_valid_bulb_around_wall:
                place_bulbs(curr[3], curr[0][1], "_", "*", "_")
                continue
            lit_up = True
            for x in range(len(puzzle)):
                if "_" not in puzzle[x]:
                    continue
                else:
                    lit_up = False
                    break
            if lit_up:
                if valid_bulbs_next_to_wall(puzzle):
                    break
            place_bulbs(curr[3], curr[0][1], "_", "*", "_")
            bulb_placed = list(curr[3])
            bulb_placed.append(curr[0][1])
            curr[1].remove(curr[0])

        for x in range(len(curr[1])):
            child_position = curr[1][x]
            child_possible_values = list(curr[1])
            if curr[0][0] == -1:
                bulb_placed = []
            stack.append((child_position,  child_possible_values, curr[2]+1, bulb_placed))


    return puzzle


def place_bulbs(existing_bulb, curr, placeholder, new, old):
    puzzle = main_puzzle
    for x in range(len(existing_bulb)):
        puzzle[existing_bulb[x][0]][existing_bulb[x][1]] = placeholder

    puzzle[curr[0]][curr[1]] = placeholder

    bulbs = list(existing_bulb)
    bulbs.append(curr)

    for x in range(len(bulbs)):
        wall_seen_u = False
        wall_seen_d = False
        wall_seen_l = False
        wall_seen_r = False

        for y in range(1, len(puzzle)):
            if bulbs[x][0] + y <= len(puzzle) - 1 and puzzle[bulbs[x][0] + y][bulbs[x][1]] == new and not wall_seen_d:
                puzzle[bulbs[x][0] + y][bulbs[x][1]] = old
            elif bulbs[x][0] + y <= len(puzzle) - 1 and (puzzle[bulbs[x][0] + y][bulbs[x][1]].isdigit()):
                wall_seen_d = True
            if bulbs[x][0] - y >= 0 and puzzle[bulbs[x][0] - y][bulbs[x][1]] == new and not wall_seen_u:
                puzzle[bulbs[x][0] - y][bulbs[x][1]] = old
            elif bulbs[x][0] - y >= 0 and (puzzle[bulbs[x][0] - y][bulbs[x][1]].isdigit()):
                wall_seen_u = True
            if bulbs[x][1] + y <= len(puzzle) - 1 and puzzle[bulbs[x][0]][bulbs[x][1] + y] == new and not wall_seen_r:
                puzzle[bulbs[x][0]][bulbs[x][1] + y] = old
            elif bulbs[x][1] + y <= len(puzzle) - 1 and (puzzle[bulbs[x][0]][bulbs[x][1] + y].isdigit()):
                wall_seen_r = True
            if bulbs[x][1] - y >= 0 and puzzle[bulbs[x][0]][bulbs[x][1] - y] == new and not wall_seen_l:
                puzzle[bulbs[x][0]][bulbs[x][1] - y] = old
            elif bulbs[x][1] - y >= 0 and (puzzle[bulbs[x][0]][bulbs[x][1] - y].isdigit()):
                wall_seen_l = True

            if wall_seen_l and wall_seen_d and wall_seen_r and wall_seen_u:
                break
    return puzzle


# This function reads in the puzzle from the text file
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


def validate_bulbs_next_to_wall(puzzle):
    for x in range(len(valid_wall)):
        num_of_bulbs = int(puzzle[valid_wall[x][0]][valid_wall[x][1]])
        valid_neighbour = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
        seen_bulbs = 0
        for z in range(len(valid_neighbour)):
            if puzzle[valid_neighbour[z][0]][valid_neighbour[z][1]] == "b":
                seen_bulbs += 1
        if num_of_bulbs < seen_bulbs:
            return False
    return True


def valid_bulbs_next_to_wall(puzzle):
    for x in range(len(valid_wall)):
        num_of_bulbs = int(puzzle[valid_wall[x][0]][valid_wall[x][1]])
        valid_neighbour = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
        seen_bulbs = 0
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
        if not puzzle[row - 1][col].isdigit():
            valid_neighbours.append([row - 1, col])
    if row < length-1:
        if not puzzle[row + 1][col].isdigit():
            valid_neighbours.append([row + 1, col])
    if col > 0:
        if not puzzle[row][col-1].isdigit():
            valid_neighbours.append([row, col - 1])
    if col < length-1:
        if not puzzle[row][col+1].isdigit():
            valid_neighbours.append([row, col + 1])

    return valid_neighbours

def count_adjacent_lit_cells(puzzle, r, c) -> int:
    count = 0
    if r > 0 and puzzle[r-1][c] == '*':
        count += 1
    if r < len(puzzle)-1 and puzzle[r+1][c] == '*':
        count += 1
    if c > 0 and puzzle[r][c-1] == '*':
        count += 1
    if c < len(puzzle[0])-1 and puzzle[r][c+1] == '*':
        count += 1
    return count


def print_puzzle(puzzle):
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            print(puzzle[x][y], end=' ')
        print()


def find_most_constraint(puzzle, child_possible_variables):
    curr_most_constrained = (-1, -1)

    for cell in child_possible_variables:
        r = cell[1][0]
        c = cell[1][1]

        adj_lit_cells = count_adjacent_lit_cells(puzzle, r, c)

        constraints = adj_lit_cells
        # randomly pick one to pick if the constraints of this cell is the same as the current most constrained
        if constraints == curr_most_constrained[0] and random.randint(0, 1) == 0:
            curr_most_constrained = (constraints, cell)
        if constraints > curr_most_constrained[0]:
            curr_most_constrained = (constraints, cell)

    return curr_most_constrained[1]


main_puzzle = read_puzzle()
prioritize_variables(main_puzzle)
print_puzzle(backtrack())
print(num_nodes)
