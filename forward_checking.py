from typing import List
import random
import light_up_puzzle
import time

wall_values = {'0', '1', '2', '3', '4'}
num_nodes = 0


def check_edge_corner(puzzle: List[List[str]], r: int, c: int) -> int:
    status = 0
    if r == 0 or r == len(puzzle) - 1:  # edge
        status += 1
    if c == 0 or c == len(puzzle[0]) - 1:  # edge, status = 2 if it's a corner
        status += 1
    return status


def get_total_potential_adjacent(puzzle: List[List[str]], r: int, c: int) -> int:
    rows, cols, count = len(puzzle), len(puzzle[0]), 0

    if r > 0 and isinstance(puzzle[r-1][c], int) and puzzle[r-1][c] >= 2:
        count += 1
    if r < rows-1 and isinstance(puzzle[r+1][c], int) and puzzle[r+1][c] >= 2:
        count += 1
    if c > 0 and isinstance(puzzle[r][c-1], int) and puzzle[r][c-1] >= 2:
        count += 1
    if c < cols-1 and isinstance(puzzle[r][c+1], int) and puzzle[r][c+1] >= 2:
        count += 1
    return count


def prioritize_bulbs(puzzle: List[List[str]], r: int, c: int):
    moving_r = r - 1
    while moving_r >= 0 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = puzzle[moving_r][c] % 2
        moving_r -= 1

    moving_r = r + 1
    while moving_r < len(puzzle)-1 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = puzzle[moving_r][c] % 2
        moving_r += 1

    moving_c = c - 1
    while moving_c >= 0 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = puzzle[r][moving_c] % 2
        moving_c -= 1

    moving_c = c + 1
    while moving_c < len(puzzle[r])-1 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = puzzle[r][moving_c] % 2
        moving_c += 1


def prioritize_walls(puzzle, r, c):
    moving_r = r - 1
    if r > 0 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = int(puzzle[moving_r][c]/2)*2
        if puzzle[moving_r][c] == 2:
            prioritize_bulbs(puzzle, moving_r, c)

    moving_r = r + 1
    if r < len(puzzle)-1 and isinstance(puzzle[moving_r][c], int):
        puzzle[moving_r][c] = int(puzzle[moving_r][c]/2) * 2
        if puzzle[moving_r][c] == 2:
            prioritize_bulbs(puzzle, moving_r, c)

    moving_c = c - 1
    if c > 0 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = int(puzzle[r][moving_c]/2) * 2
        if puzzle[r][moving_c] == 2:
            prioritize_bulbs(puzzle, r, moving_c)

    moving_c = c + 1
    if c < len(puzzle[0])-1 and isinstance(puzzle[r][moving_c], int):
        puzzle[r][moving_c] = int(puzzle[r][moving_c]/2) * 2
        if puzzle[r][moving_c] == 2:
            prioritize_bulbs(puzzle, r, moving_c)


def generate_potential_bulbs_to_wall(puzzle: List[List[int]], r: int, c: int) -> int:
    num_bulbs = 0
    if r > 0 and isinstance(puzzle[r-1][c], int) and puzzle[r-1][c] >= 2:
        num_bulbs += 1
    if r < len(puzzle)-1 and isinstance(puzzle[r+1][c], int) and puzzle[r+1][c] >= 2:
        num_bulbs += 1
    if c > 0 and isinstance(puzzle[r][c-1], int) and puzzle[r][c-1] >= 2:
        num_bulbs += 1
    if c < len(puzzle[0])-1 and isinstance(puzzle[r][c+1], int) and puzzle[r][c+1] >= 2:
        num_bulbs += 1
    return num_bulbs


def check_curr_state(puzzle, non_assigned_cells) -> bool:
    # if a cell can be a bulb or empty, mark it as 3
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            value = len(puzzle)*r + c
            if value in non_assigned_cells:
                puzzle[r][c] = 3

    # if a cell cannot be a bulb, mark it as 1.
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == 'b':
                prioritize_bulbs(puzzle, r, c)

    # if a cell cannot be empty but can be a bulb, mark it as 2, mark it as 0 if it can't be neither
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


def is_inside(puzzle: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(puzzle) and 0 <= c < len(puzzle[0])


def can_bulb_be_here(puzzle: List[List[str]], r: int, c: int) -> bool:
    delta_r = [-1, 1, 0, 0]
    delta_c = [0, 0, -1, 1]
    for i in range(len(delta_c)):
        moving_r = r + delta_r[i]
        moving_c = c + delta_c[i]

        if is_inside(puzzle, moving_r, moving_c) and puzzle[moving_r][moving_c] in wall_values:
            if count_adjacent_bulbs(puzzle, moving_r, moving_c) > int(puzzle[moving_r][moving_c]):
                return False

        while is_inside(puzzle, moving_r, moving_c) and not puzzle[moving_r][moving_c] in wall_values:
            if puzzle[moving_r][moving_c] == 'b':  # adjacent bulbs
                return False
            moving_r += delta_r[i]
            moving_c += delta_c[i]
    return True


def forward_checking(puzzle: List[List[str]], domain, non_assigned_cells, heuristic='most_constrained'):
    global num_nodes
    num_nodes += 1
    if num_nodes % 10000 == 0:
        print(num_nodes)
    if num_nodes == 5000000:
        return 'Too many nodes. Timeout'
    if is_puzzle_solved(puzzle):
        return puzzle
    if len(non_assigned_cells) == 0 and check_curr_state(puzzle, non_assigned_cells):
        return 'back'
    most_constrained = find_most_constrained(puzzle, non_assigned_cells)
    non_assigned_cells.remove(most_constrained)

    r, c = most_constrained[0], most_constrained[1]
    for val in domain:
        puzzle[r][c] = val
        if (val != '_' and can_bulb_be_here(puzzle, r, c)) or val == '_':
            result = forward_checking(puzzle, domain, non_assigned_cells, heuristic='most_constrained')
            if result != 'back':
                return result

    non_assigned_cells.append(most_constrained)
    return 'back'


def count_adjacent_bulbs(puzzle: List[List[str]], r: int, c: int) -> int:
    num_bulbs = 0
    if r > 0 and puzzle[r-1][c] == 'b':
        num_bulbs += 1
    if r < len(puzzle)-1 and puzzle[r+1][c] == 'b':
        num_bulbs += 1
    if c > 0 and puzzle[r][c-1] == 'b':
        num_bulbs += 1
    if c < len(puzzle[0])-1 and puzzle[r][c+1] == 'b':
        num_bulbs += 1
    return num_bulbs


# check if the current solution is valid
def is_puzzle_solved(puzzle: List[List[str]]) -> bool:
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] in wall_values and int(puzzle[r][c]) != count_adjacent_bulbs(puzzle, r, c):
                return False

    light_map_up(puzzle)

    # TODO: probably should print the solution here
    return is_map_lit_up_and_clean_map(puzzle)


def light_map_up(puzzle: List[List[str]]):
    for r in range(len(puzzle)):
        for c in range(len(puzzle[0])):
            if puzzle[r][c] == 'b':
                k = 1
                while r - k >= 0 and (puzzle[r-k][c] == '_' or puzzle[r - k][c] == '*'):
                    puzzle[r-k][c] = '*'
                    k += 1
                k = 1
                while r + k < len(puzzle) and (puzzle[r + k][c] == '_' or puzzle[r + k][c] == '*'):
                    puzzle[r + k][c] = '*'
                    k += 1
                k = 1
                while c - k >= 0 and (puzzle[r][c - k] == '_' or puzzle[r][c - k] == '*'):
                    puzzle[r][c - k] = '*'
                    k += 1
                k = 1
                while c + k < len(puzzle[r]) and (puzzle[r][c + k] == '_' or puzzle[r][c + k] == '*'):
                    puzzle[r][c + k] = '*'
                    k += 1


# given a bulb position, count the number of cells should be lit up in the corresponding row and column
def num_cells_should_be_lit(puzzle: List[List[str]], r: int, c: int) -> int:
    num_cells = 0
    row_up = r - 1
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


def count_walls_around(puzzle: List[List[str]], r: int, c: int) -> int:
    num_walls = 0
    if r > 0 and puzzle[r-1][c] in wall_values:
        num_walls += int(int(puzzle[r-1][c])/2 + 1)
    if r < len(puzzle)-1 and puzzle[r+1][c] in wall_values:
        num_walls += int(int(puzzle[r+1][c])/2 + 1)
    if c > 0 and puzzle[r][c-1] in wall_values:
        num_walls += int(int(puzzle[r][c-1])/2 + 1)
    if c < len(puzzle[0])-1 and puzzle[r][c+1] in wall_values:
        num_walls += int(int(puzzle[r][c+1])/2 + 1)
    return num_walls


def count_adjacent_lit_cells(puzzle: List[List[str]], r, c) -> int:
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


def is_map_lit_up_and_clean_map(puzzle: List[List[str]]) -> bool:
    lit_up = True
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == '_':  # the solution is not valid
                lit_up = False
            elif puzzle[r][c] == '*':
                puzzle[r][c] = '_'
    return lit_up


def find_most_constrained(puzzle: List[List[str]], empty_cells: List[List[int]]) -> int:
    curr_most_constrained = (-1, -1)
    light_map_up(puzzle)

    for cell in empty_cells:
        r = cell[0]
        c = cell[1]

        num_walls = count_walls_around(puzzle, r, c)
        # check to see if a cell is in an edge, or corner
        location = check_edge_corner(puzzle, r, c)
        adj_lit_cells = count_adjacent_lit_cells(puzzle, r, c)

        constraints = num_walls + location + adj_lit_cells
        # randomly pick one to pick if the constraints of this cell is the same as the current most constrained
        if constraints == curr_most_constrained[0] and random.randint(0, 1) == 0:
            curr_most_constrained = (constraints, cell)
        if constraints > curr_most_constrained[0]:
            curr_most_constrained = (constraints, cell)

    is_map_lit_up_and_clean_map(puzzle)
    return curr_most_constrained[1]


def find_most_constraining(puzzle: List[List[str]], empty_cells: List[List[int]]):
    cells = []
    max_count = 0

    light_map_up(puzzle)

    for cell in empty_cells:
        r = cell[0]
        c = cell[1]
        to_be_lit_up = num_cells_should_be_lit(puzzle, r, c)
        if to_be_lit_up > max_count:
            cells = [cell]
            max_count = to_be_lit_up
        elif to_be_lit_up == max_count:
            cells.append(cell)
    is_map_lit_up_and_clean_map(puzzle)
    return cells[random.randint(0, len(cells)-1)]


def get_empty_cells(puzzle: List[List[str]]) -> List[List[int]]:
    empty_cells = []
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
            if puzzle[r][c] == '_':
                empty_cells.append([r, c])
    return empty_cells


def solve(puzzle: List[List[str]]):
    domain = ('b', '_')
    non_assigned = get_empty_cells(puzzle)
    return forward_checking(puzzle, domain, non_assigned)


def print_puzzle(puzzle: List[List[str]]):
    for r in range(len(puzzle)):
        for c in range(len(puzzle[0])):
            print(puzzle[r][c], end=' ')
        print()


# TODO: add different input reading methods and heuristic detection
puzzle = light_up_puzzle.read_puzzle()
# print(type(puzzle))
starting_time = time.time()
solution = solve(puzzle)
ending_time = time.time()
if solution == 'Too many nodes. Timeout':
    print('Too many nodes. Timeout.\nIt took {} seconds.'.format(ending_time - starting_time))
else:
    print_puzzle(solution)
    print("The puzzle was solved in {} seconds.".format(ending_time - starting_time))
print('Visited {} nodes.'.format(num_nodes))
