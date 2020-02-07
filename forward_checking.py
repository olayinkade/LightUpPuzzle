import argparse
import sys
from typing import List
import random
import library
import time
import copy

wall_values = {'0', '1', '2', '3', '4'}
num_nodes = 0


# check if a cell is in a special place, such as on the edge or in the corner
# assign different status/priority values for further processing later
def check_edge_corner(puzzle: List[List[str]], r: int, c: int) -> int:
    status = 0
    if r == 0 or r == len(puzzle) - 1:  # edge
        status += 1
    if c == 0 or c == len(puzzle[0]) - 1:  # edge, status = 2 if it's a corner
        status += 1
    return status


def prioritize_bulbs(puzzle, r: int, c: int):
    moving_r = r - 1
    while moving_r >= 0 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = puzzle[moving_r][c] % 2
        moving_r -= 1

    moving_r = r + 1
    while moving_r < len(puzzle) - 1 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = puzzle[moving_r][c] % 2
        moving_r += 1

    moving_c = c - 1
    while moving_c >= 0 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = puzzle[r][moving_c] % 2
        moving_c -= 1

    moving_c = c + 1
    while moving_c < len(puzzle[r]) - 1 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = puzzle[r][moving_c] % 2
        moving_c += 1


def prioritize_walls(puzzle, r, c):
    moving_r = r - 1
    if r > 0 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = int(puzzle[moving_r][c] / 2) * 2
        if puzzle[moving_r][c] == 2:
            prioritize_bulbs(puzzle, moving_r, c)

    moving_r = r + 1
    if r < len(puzzle) - 1 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = int(puzzle[moving_r][c] / 2) * 2
        if puzzle[moving_r][c] == 2:
            prioritize_bulbs(puzzle, moving_r, c)

    moving_c = c - 1
    if c > 0 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = int(puzzle[r][moving_c] / 2) * 2
        if puzzle[r][moving_c] == 2:
            prioritize_bulbs(puzzle, r, moving_c)

    moving_c = c + 1
    if c < len(puzzle[0]) - 1 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = int(puzzle[r][moving_c] / 2) * 2
        if puzzle[r][moving_c] == 2:
            prioritize_bulbs(puzzle, r, moving_c)


# check to see among all adjacent cells, how many are potential places for bulbs,
# >=2 as empty with priority 2 can be bulbs
def generate_potential_bulbs_to_wall(puzzle, r: int, c: int) -> int:
    num_bulbs = 0
    # check all for neighbours
    if r > 0 and isinstance(puzzle[r - 1][c], int) and puzzle[r - 1][c] >= 2:
        num_bulbs += 1
    if r < len(puzzle) - 1 and isinstance(puzzle[r + 1][c], int) and puzzle[r + 1][c] >= 2:
        num_bulbs += 1
    if c > 0 and isinstance(puzzle[r][c - 1], int) and puzzle[r][c - 1] >= 2:
        num_bulbs += 1
    if c < len(puzzle[0]) - 1 and isinstance(puzzle[r][c + 1], int) and puzzle[r][c + 1] >= 2:
        num_bulbs += 1
    return num_bulbs


# check the status of the current "solution", or node, to see if it could be on the path to the solution,
# return False if it cannot be possibly part of a solution
def check_curr_state(puzzle, non_assigned_cells) -> bool:
    # if a cell can be a bulb or empty, its priority is 3
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            value = len(puzzle) * r + c
            if value in non_assigned_cells:
                puzzle[r][c] = 3

    # if a cell cannot be a bulb, its priority is 1.
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == 'b':
                prioritize_bulbs(puzzle, r, c)

    # if a cell cannot be empty but can be a bulb, assign 2 as its priority,
    # priority 0 if it can't be neither
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] in wall_values:
                num_adj_bulbs = count_adjacent_bulbs(puzzle, r, c)
                potential_bulbs = generate_potential_bulbs_to_wall(puzzle, r, c)
                cell_status = check_edge_corner(puzzle, r, c)

                require_bulbs = int(puzzle[r][c]) - num_adj_bulbs - cell_status
                if require_bulbs == potential_bulbs:
                    prioritize_walls(puzzle, r, c)

    result = True
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if isinstance(puzzle[r][c], int):
                if puzzle[r][c] == 0:
                    result = False
                puzzle[r][c] = '_'
    return result


# check if a given cell is inside the map
def is_inside(puzzle: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(puzzle) and 0 <= c < len(puzzle[0])


# given a cell, check if we can place a bulb there
def can_bulb_be_here(puzzle: List[List[str]], r: int, c: int) -> bool:
    delta_r = [-1, 1, 0, 0]
    delta_c = [0, 0, -1, 1]
    for i in range(len(delta_c)):
        moving_r = r + delta_r[i]
        moving_c = c + delta_c[i]

        if is_inside(puzzle, moving_r, moving_c) and puzzle[moving_r][moving_c] in wall_values:
            # if there is already enough number of bulbs for that well
            if count_adjacent_bulbs(puzzle, moving_r, moving_c) > int(puzzle[moving_r][moving_c]):
                return False

        while is_inside(puzzle, moving_r, moving_c) and not puzzle[moving_r][moving_c] in wall_values:
            if puzzle[moving_r][moving_c] == 'b':  # adjacent bulbs
                return False
            moving_r += delta_r[i]
            moving_c += delta_c[i]
    return True


# count the number of neighbouring bulbs surrounding a cell
def count_adjacent_bulbs(puzzle: List[List[str]], r: int, c: int) -> int:
    num_bulbs = 0
    if r > 0 and puzzle[r - 1][c] == 'b':
        num_bulbs += 1
    if r < len(puzzle) - 1 and puzzle[r + 1][c] == 'b':
        num_bulbs += 1
    if c > 0 and puzzle[r][c - 1] == 'b':
        num_bulbs += 1
    if c < len(puzzle[0]) - 1 and puzzle[r][c + 1] == 'b':
        num_bulbs += 1
    return num_bulbs


# given a map with newly placed bulbs, light up every corresponding cell in the same row and column with * symbol
def light_map_up(puzzle: List[List[str]]):
    for r in range(len(puzzle)):
        for c in range(len(puzzle[0])):
            if puzzle[r][c] == 'b':
                # loop through all cells in the same row and column with the current bulb
                dist = 1
                while r - dist >= 0 and (puzzle[r - dist][c] == '_' or puzzle[r - dist][c] == '*'):
                    puzzle[r - dist][c] = '*'
                    dist += 1
                dist = 1
                while r + dist < len(puzzle) and (puzzle[r + dist][c] == '_' or puzzle[r + dist][c] == '*'):
                    puzzle[r + dist][c] = '*'
                    dist += 1
                dist = 1
                while c - dist >= 0 and (puzzle[r][c - dist] == '_' or puzzle[r][c - dist] == '*'):
                    puzzle[r][c - dist] = '*'
                    dist += 1
                dist = 1
                while c + dist < len(puzzle[r]) and (puzzle[r][c + dist] == '_' or puzzle[r][c + dist] == '*'):
                    puzzle[r][c + dist] = '*'
                    dist += 1


# check if the current solution is valid
def validate_wall_condition(puzzle: List[List[str]]) -> bool:
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] in wall_values and int(puzzle[r][c]) != count_adjacent_bulbs(puzzle, r, c):
                return False

    light_map_up(puzzle)

    library.print_puzzle(puzzle)
    print("--------------")
    return is_map_lit_up_and_clean_map(puzzle)


# given a bulb position, count the number of cells should be lit up in the corresponding row and column
# return the number of cells that would be lit up
def num_cells_should_be_lit(puzzle: List[List[str]], r: int, c: int) -> int:
    num_cells = 0
    row_up = r - 1
    # loop through all four directions
    while row_up >= 0 and (puzzle[row_up][c] == '_' or puzzle[row_up][c] == '*'):
        if puzzle[row_up][c] == '_':
            num_cells += 1
        row_up -= 1

    row_down = r + 1
    while row_down < len(puzzle) and (puzzle[row_down][c] == '_' or puzzle[row_down][c] == '*'):
        if puzzle[row_down][c] == '_':
            num_cells += 1
        row_down += 1

    col_left = c - 1
    while col_left >= 0 and (puzzle[r][col_left] == '_' or puzzle[r][col_left] == '*'):
        if puzzle[r][col_left] == '_':
            num_cells += 1
        col_left -= 1

    col_right = c + 1
    while col_right < len(puzzle[0]) and (puzzle[r][col_right] == '_' or puzzle[r][col_right] == '*'):
        if puzzle[r][col_right] == '_':
            num_cells += 1
        col_right += 1

    return num_cells


# count number of walls around a cell, this plays an important role in the constraint of a cell (variable).
# if its neighbouring wall is 3 or 4, there is a higher chance that it has to be a bulb than if its neighbouring
# wall is a 0, 1 or 2.
def count_walls_around(puzzle: List[List[str]], r: int, c: int) -> int:
    num_walls = 0
    if r > 0 and puzzle[r - 1][c] in wall_values:
        num_walls += int(int(puzzle[r - 1][c]) / 2 + 1)
    if r < len(puzzle) - 1 and puzzle[r + 1][c] in wall_values:
        num_walls += int(int(puzzle[r + 1][c]) / 2 + 1)
    if c > 0 and puzzle[r][c - 1] in wall_values:
        num_walls += int(int(puzzle[r][c - 1]) / 2 + 1)
    if c < len(puzzle[0]) - 1 and puzzle[r][c + 1] in wall_values:
        num_walls += int(int(puzzle[r][c + 1]) / 2 + 1)
    return num_walls


# count the number of lit up cells out of its 4 neighbours.
def count_adjacent_lit_cells(puzzle: List[List[str]], r, c) -> int:
    count = 0
    if r > 0 and puzzle[r - 1][c] == '*':
        count += 1
    if r < len(puzzle) - 1 and puzzle[r + 1][c] == '*':
        count += 1
    if c > 0 and puzzle[r][c - 1] == '*':
        count += 1
    if c < len(puzzle[0]) - 1 and puzzle[r][c + 1] == '*':
        count += 1
    if puzzle[r][c] == '*':  # if it itself is lit up
        count += 3
    return count


# check if the map is completely lit up, if not then the solution is not complete, return False
# clean the map (remove star symbol) to be printed out.
def is_map_lit_up_and_clean_map(puzzle: List[List[str]]) -> bool:
    lit_up = True
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == '_':  # the solution is not valid
                lit_up = False
            elif puzzle[r][c] == '*':
                puzzle[r][c] = '_'

    return lit_up


# choose (a) cell(s) to place a bulb, based on most constrained heuristic
# criteria for constraints: number of walls surrounding the cell, its location (if it's in the middle or on the
# edge/corner, and if its neighbours are lit up.
def find_most_constrained(puzzle: List[List[str]], empty_cells: List[List[int]]):
    curr_most_constrained = (-1, [])
    light_map_up(puzzle)

    for cell in empty_cells:
        num_walls = count_walls_around(puzzle, cell[0], cell[1])
        # check to see if a cell is in an edge, or corner
        location = check_edge_corner(puzzle, cell[0], cell[1])
        adj_lit_cells = count_adjacent_lit_cells(puzzle, cell[0], cell[1])

        constraints = num_walls + location + adj_lit_cells

        # add current cells to the list if the constraints of this cell is the same as the current most constrained
        if constraints == curr_most_constrained[0]:
            curr_most_constrained[1].append(cell)
        if constraints > curr_most_constrained[0]:
            curr_most_constrained = (constraints, [cell])

    is_map_lit_up_and_clean_map(puzzle)
    return curr_most_constrained[1]


# choose (a) cell(s) to place a bulb, based on most constraining heuristic
# criterion: number of cells would be lit up if we placed a bulb in a certain cell.
def find_most_constraining(puzzle: List[List[str]], empty_cells: List[List[int]]):
    cells = []
    max_count = 0

    light_map_up(puzzle)

    for cell in empty_cells:
        to_be_lit_up = num_cells_should_be_lit(puzzle, cell[0], cell[1])
        if to_be_lit_up > max_count:
            cells = [cell]
            max_count = to_be_lit_up
        elif to_be_lit_up == max_count:
            cells.append(cell)
    is_map_lit_up_and_clean_map(puzzle)
    return cells


# this is a combination of most constrained and most constraining heuristics, with most constraining heuristic acts as a
# tie breaker for most constrained heuristic.
def hybrid_heuristic(puzzle: List[List[str]], empty_cells: List[List[int]]):
    chosen_cells = find_most_constrained(puzzle, empty_cells)
    # when there is a tie between multiple empty cells
    if len(chosen_cells) > 1:
        chosen_cells = find_most_constraining(puzzle, chosen_cells)
    is_map_lit_up_and_clean_map(puzzle)
    return chosen_cells


# forward checking algorithm, with corresponding heuristic
def forward_checking(puzzle: List[List[str]], domain, empty_cells, heuristic: str):
    global num_nodes
    num_nodes += 1
    # printing solving status
    if num_nodes < 10000:
        if num_nodes % 3 == 0:
            print('\rProcessing.', end='')
        if num_nodes % 3 == 1:
            print('\rProcessing..', end='')
        if num_nodes % 3 == 2:
            print('\rProcessing...', end='')
    if num_nodes % 10000 == 0:
        print('\rAlready processed {} nodes.'.format(num_nodes), end='')
    if num_nodes == 5000000:
        return 'Too many nodes. Timeout!'
    if validate_wall_condition(puzzle):
        return puzzle
    # backtrack if this cannot be part of a valid solution
    if len(empty_cells) == 0 and check_curr_state(puzzle, empty_cells):
        return 'backtrack'

    chosen_cells, chosen_cell = [], []
    # check the input to see what heuristic should be used
    if heuristic == 'most_constrained':
        chosen_cells = find_most_constrained(puzzle, empty_cells)
    elif heuristic == 'most_constraining':
        chosen_cells = find_most_constraining(puzzle, empty_cells)
    elif heuristic == 'hybrid':
        chosen_cells = hybrid_heuristic(puzzle, empty_cells)
    else:
        print('\n*** ERROR *** Heuristic must be either "most_constrained", "most_constraining" or "hybrid".')
        return 'stop'
    if len(chosen_cells) >= 1:
        chosen_cell = chosen_cells[random.randint(0, len(chosen_cells) - 1)]

    # remove the chosen cell from the list of potential bulb cells later
    empty_cells.remove(chosen_cell)

    r, c = chosen_cell[0], chosen_cell[1]
    for val in domain:
        puzzle[r][c] = val
        if (val != '_' and can_bulb_be_here(puzzle, r, c)) or val == '_':
            result = forward_checking(puzzle, domain, empty_cells, heuristic)
            if result != 'backtrack':
                return result

    empty_cells.append(chosen_cell)
    return 'backtrack'


# get all the empty cells in the map, which are potential places for bulbs.
def get_empty_cells(puzzle: List[List[str]]) -> List[List[int]]:
    empty_cells = []
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == '_':
                empty_cells.append([r, c])
    return empty_cells


# some places in the map are certain to be bulbs because of some constraints, for example neighbours of a wall 4 have to
# bulbs, neighbours of wall 3 in the edge, neighbours of wall 2 in the corner, or the amount of empty neighbours of a
# wall is exactly the same as its number.
def place_must_have_bulbs(puzzle: List[List[str]], empty_cells: List[List[int]]) -> List[List[int]]:
    stop = False
    while not stop:
        new_bulb_placed = False
        for wall in library.valid_wall:

            sure_variable = library.generate_valid_neighbours(wall[0], wall[1], len(puzzle), puzzle)
            count_bulbs = 0
            count_empty_cells = 0
            count_stars = 0
            for var in sure_variable:
                if puzzle[var[0]][var[1]] == 'b':
                    count_bulbs += 1
                elif puzzle[var[0]][var[1]] == '_':
                    count_empty_cells += 1
                elif puzzle[var[0]][var[1]] == '*':
                    count_stars += 1
            # if the amount of empty neighbours of a wall is exactly the same as its number, place bulbs
            if count_empty_cells > 0 and count_empty_cells == int(puzzle[wall[0]][wall[1]]) - count_bulbs:
                for var in sure_variable:
                    if puzzle[var[0]][var[1]] == '_':
                        puzzle[var[0]][var[1]] = 'b'
                        empty_cells.remove(var)

                new_bulb_placed = True
                light_map_up(puzzle)
        if not new_bulb_placed:
            stop = True

    # remove already lit up cells from the list of potential cells to place a bulb
    variables = copy.deepcopy(empty_cells)
    for cell in variables:
        if puzzle[cell[0]][cell[1]] == '*':
            empty_cells.remove(cell)

    return empty_cells


# remove all cells surrounding a wall 0 from the list of places for bulbs, as there can't be any bulbs surrouding
# a wall 0
def remove_zero_wall_neighbours(puzzle: List[List[str]], empty_cells: List[List[int]]):
    invalid_neighbours = []
    # remove all neighbours of a zero wall
    for x in range(len(library.invalid_wall)):
        invalid_neighbours.extend(library.generate_valid_neighbours(library.invalid_wall[x][0],
                                                                    library.invalid_wall[x][1], len(puzzle), puzzle))
    for x in range(len(invalid_neighbours)):
        if invalid_neighbours[x] in empty_cells:
            empty_cells.remove(invalid_neighbours[x])


# do some pre-processing to decrease the number of variables to be considered
def pre_process(puzzle: List[List[str]], empty_cells: List[List[int]]):
    empty_cells = place_must_have_bulbs(puzzle, empty_cells)
    remove_zero_wall_neighbours(puzzle, empty_cells)
    # TODO: Remove this print line
    library.print_puzzle(puzzle)
    is_map_lit_up_and_clean_map(puzzle)


# call necessary methods/algorithms to solve the puzzle as required.
def solve(puzzle: List[List[str]], heuristic: str):
    domain = ('b', '_')
    non_assigned = get_empty_cells(puzzle)
    pre_process(puzzle, non_assigned)
    print("Chosen heuristic: {}.".format(heuristic))
    return forward_checking(puzzle, domain, non_assigned, heuristic)


# receive input, process input and call necessary methods to solve the puzzle.
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--heuristic', action='store', dest='heuristic', type=str, default='most_constrained')

    arguments = arg_parser.parse_args(argv)

    puzzle = library.read_puzzle()

    starting_time = time.time()
    solution = solve(puzzle, arguments.heuristic)
    ending_time = time.time()
    if solution == 'Too many nodes. Timeout!':
        print('Too many nodes. Timeout.\nIt took {} seconds.'.format(ending_time - starting_time))
    elif solution == 'stop':
        print('Please retry!')
    else:
        print('*** Done! ***\nThe solution is printed out below:')
        library.print_puzzle(solution)
        print("The puzzle was solved in {} seconds.".format(ending_time - starting_time))
    print('Visited {} nodes.'.format(num_nodes))


if __name__ == '__main__':
    main()
