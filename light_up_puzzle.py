import random
stack = []
variables = []
invalid_wall = []
valid_wall = []
already_placed = []


def prioritize_by_wall_neighbours(puzzle):
    # Prioritize empty position where walls are valid neighbours
    for x in variables:
        x[0] = 0

    for x in range(len(valid_wall)):
        valid_neighbours = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
        if int(puzzle[valid_wall[x][0]][valid_wall[x][1]]) != count_bulbs(puzzle, valid_wall[x]):
            for z in range(len(valid_neighbours)):
                for a in range(len(variables)):
                    if variables[a][1] == valid_neighbours[z]:
                        variables[a][0] += 1
                        break
        else:
            for z in range(len(valid_neighbours)):
                for a in range(len(variables)):
                    if variables[a][1] == valid_neighbours[z]:
                        variables[a][0] -= 2
                        break


def remove_zero_wall_neighbours(puzzle):
    invalid_neighbours = []
    # remove all neighbours of a zero wall
    for x in range(len(invalid_wall)):
        invalid_neighbours.extend(generate_valid_neighbours(invalid_wall[x][0],
                                                            invalid_wall[x][1], len(puzzle), puzzle))
    for x in range(len(invalid_neighbours)):
        for y in range(len(variables)):
            if variables[y][1] == invalid_neighbours[x]:
                variables.remove(variables[y])
                break


def count_bulbs(puzzle, wall):
    counter = 0
    sure_variable = generate_valid_neighbours(wall[0], wall[1], len(puzzle), puzzle)
    for x in sure_variable:
        if puzzle[x[0]][x[1]] == "b":
            counter += 1
    return counter


def place_sure_bulbs(puzzle):
    not_changed = False
    count = 0
    while not not_changed:
        removed = False
        for x in range(len(valid_wall)):

            value = puzzle[valid_wall[x][0]][valid_wall[x][1]]
            if count == 0:
                sure_variable = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
            else:
                sure_variable = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle, True)
            add = True
            counter = count_bulbs(puzzle, valid_wall[x])
            if count > 0 and counter == int(value):
                add = False

            if int(value) >= len(sure_variable) + counter:
                for y in range(len(sure_variable)):
                    if sure_variable[y] not in already_placed and add:
                        already_placed.append(sure_variable[y])
                    for z in range(len(variables)):
                        if variables[z][1] == sure_variable[y]:
                            variables.remove(variables[z])
                            removed = True
                            break
        count += 1
        if not removed:
            not_changed = True
        place_bulbs(already_placed, [], "b", "_", "*")


def remove_variables_that_is_lit(puzzle):
    variables_with_star = []
    for x in variables:
        if puzzle[x[1][0]][x[1][1]] == "*":
            variables_with_star.append(x)

    for x in variables_with_star:
        variables.remove(x)


def remove_completed_wall(puzzle):
    completed_walls = []
    for x in range(len(valid_wall)):
        if count_bulbs(puzzle, valid_wall[x]) == int(puzzle[valid_wall[x][0]][valid_wall[x][1]]):
            completed_walls.append(valid_wall[x])
            valid_neighbours_a = generate_valid_neighbours(valid_wall[x][0], valid_wall[x][1], len(puzzle), puzzle)
            for var in valid_neighbours_a:
                for cells in variables:
                    if cells[1] == var:
                        variables.remove(cells)

    for wall in completed_walls:
        valid_wall.remove(wall)


def prioritize_variables(puzzle):
    remove_zero_wall_neighbours(puzzle)
    place_sure_bulbs(puzzle)
    remove_variables_that_is_lit(place_bulbs(already_placed, [], "b", "_", "*"))
    lit_up = is_lit_up(puzzle)
    remove_completed_wall(puzzle)
    prioritize_by_wall_neighbours(puzzle)
    variables.sort()

    return lit_up


def is_lit_up(puzzle):
    lit_up = True
    for x in range(len(puzzle)):
        if "_" not in puzzle[x]:
            continue
        else:
            lit_up = False
            break
    return lit_up


def backtrack():
    stack.append(([-1, -1], variables, 0, already_placed))
    global num_nodes
    num_nodes = 1
    while len(stack) != 0:
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
            if is_lit_up(puzzle):
                if valid_bulbs_next_to_wall(puzzle):
                    break

            bulb_placed = list(curr[3])
            bulb_placed.append(curr[0][1])
            puzzle = place_bulbs(curr[3], curr[0][1], "b", "_", "*")
            curr[1].remove(curr[0])

        find_most_constraining(main_puzzle, curr[1])

        for x in range(len(curr[1])):
            child_position = curr[1][x]
            child_possible_values = list(curr[1])
            if curr[0][0] == -1:
                bulb_placed = already_placed
            stack.append((child_position,  child_possible_values, curr[2]+1, bulb_placed))

    return puzzle


def place_bulbs(existing_bulb, curr, placeholder, new, old):
    puzzle = main_puzzle
    for x in range(len(existing_bulb)):
        puzzle[existing_bulb[x][0]][existing_bulb[x][1]] = placeholder

    if len(curr) != 0:
        puzzle[curr[0]][curr[1]] = placeholder

    bulbs = list(existing_bulb)
    if len(curr) != 0:
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


def num_cells_lit(curr, new):
    puzzle = main_puzzle
    num_lit = 0

    wall_seen_u = False
    wall_seen_d = False
    wall_seen_l = False
    wall_seen_r = False

    for y in range(1, len(puzzle)):
        if curr[0] + y <= len(puzzle) - 1 and puzzle[curr[0] + y][curr[1]] == new and not wall_seen_d:
            num_lit += 1
        elif curr[0] + y <= len(puzzle) - 1 and (puzzle[curr[0] + y][curr[1]].isdigit()):
            wall_seen_d = True
        if curr[0] - y >= 0 and puzzle[curr[0] - y][curr[1]] == new and not wall_seen_u:
            num_lit += 1
        elif curr[0] - y >= 0 and (puzzle[curr[0] - y][curr[1]].isdigit()):
            wall_seen_u = True
        if curr[1] + y <= len(puzzle) - 1 and puzzle[curr[0]][curr[1] + y] == new and not wall_seen_r:
            num_lit += 1
        elif curr[1] + y <= len(puzzle) - 1 and (puzzle[curr[0]][curr[1] + y].isdigit()):
            wall_seen_r = True
        if curr[1] - y >= 0 and puzzle[curr[0]][curr[1] - y] == new and not wall_seen_l:
            num_lit += 1
        elif curr[1] - y >= 0 and (puzzle[curr[0]][curr[1] - y].isdigit()):
            wall_seen_l = True
        if wall_seen_l and wall_seen_d and wall_seen_r and wall_seen_u:
            break
    return num_lit


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


def count_adjacent_lit_cells(puzzle, r, c) -> int:
    count = 0
    if r > 0 and (puzzle[r-1][c] == '*' or puzzle[r-1][c] == 'b'):
        count += 1
    if r < len(puzzle)-1 and (puzzle[r+1][c] == '*' or puzzle[r+1][c] == 'b') :
        count += 1
    if c > 0 and (puzzle[r][c-1] == '*' or puzzle[r][c-1] == 'b'):
        count += 1
    if c < len(puzzle[0])-1 and (puzzle[r][c+1] == '*' or puzzle[r][c+1] == 'b'):
        count += 1
    if puzzle[r][c] == '*':
        count += 2

    return count


def print_puzzle(puzzle):
    for x in range(len(puzzle)):
        for y in range(len(puzzle)):
            print(puzzle[x][y], end=' ')
        print()


def find_most_constrained(puzzle, child_possible_variables):
    prioritize_by_wall_neighbours(puzzle)
    for cell in child_possible_variables:
        r = cell[1][0]
        c = cell[1][1]
        constraints = -1
        adj_lit_cells = count_adjacent_lit_cells(puzzle, r, c)
        for var in variables:
            if var[1][0] == r and var[1][1] == c:
                constraints = var[0]
                break
        constraints += adj_lit_cells
        cell[0] = constraints

    child_possible_variables.sort()

    max = child_possible_variables[-1][0]
    y = -1
    for cell in child_possible_variables:
        if max == cell[0]:
            y += 1
    chosen = random.randint(0, y) * -1

    item_1 = child_possible_variables[-1]
    child_possible_variables[-1] = child_possible_variables[-1 + chosen]
    child_possible_variables[-1 + chosen] = item_1


def find_most_constraining(puzzle, child_possible_variables):
    prioritize_by_wall_neighbours(puzzle)
    for cell in child_possible_variables:
        r = cell[1][0]
        c = cell[1][1]
        constraints = -1
        num_lit = num_cells_lit(cell[1], "_")
        for var in variables:
            if var[1][0] == r and var[1][1] == c:
                constraints = var[0]
                break
        constraints += num_lit
        cell[0] = constraints
    for wall in valid_wall:
        possible_position = generate_valid_neighbours(wall[0], wall[1], len(puzzle), puzzle, True)
        if int(puzzle[wall[0]][wall[1]]) > count_bulbs(puzzle, wall):
            for poss in possible_position:
                for cell in child_possible_variables:
                    if cell[1] == poss:
                        cell[0] += 3

    child_possible_variables.sort()

    max = child_possible_variables[-1][0]
    y = -1
    for cell in child_possible_variables:
        if max == cell[0]:
            y += 1
    chosen = random.randint(0, y) * -1

    item_1 = child_possible_variables[-1]
    child_possible_variables[-1] = child_possible_variables[-1 + chosen]
    child_possible_variables[-1 + chosen] = item_1


def hybrid(puzzle, child_possible_variables):
    prioritize_by_wall_neighbours(puzzle)

    for cell in child_possible_variables:
        r = cell[1][0]
        c = cell[1][1]
        constraints = -1
        adj_lit_cells = count_adjacent_lit_cells(puzzle, r, c)
        num_lit = num_cells_lit(cell[1], "_")
        for var in variables:
            if var[1][0] == r and var[1][1] == c:
                constraints = var[0]
                break
        constraints += adj_lit_cells + num_lit
        cell[0] = constraints

    child_possible_variables.sort()

    max = child_possible_variables[-1][0]
    y = -1
    for cell in child_possible_variables:
        if max == cell[0]:
            y += 1
    chosen = random.randint(0, y) * -1

    item_1 = child_possible_variables[-1]
    child_possible_variables[-1] = child_possible_variables[-1 + chosen]
    child_possible_variables[-1 + chosen] = item_1


main_puzzle = read_puzzle()
if not prioritize_variables(main_puzzle):
    print_puzzle(backtrack())
    print(num_nodes)
else:
    print_puzzle(main_puzzle)

print("Done")
