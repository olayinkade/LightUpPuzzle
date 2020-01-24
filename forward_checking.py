from typing import List
import random

wall_values = {'0', '1', '2', '3', '4'}


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



def forward_checking(puzzle: List[List[str]], domain, non_assigned_cells, heuristic):
    num_nodes = 0
    result = ""
    if num_nodes % 10000 == 0:
        print(num_nodes)
    if num_nodes == 5000000:
        result = 'Too many nodes. Timeout'
    if is_puzzle_solved(puzzle):
        return puzzle
    # if len(non_assigned_cells) == 0 and


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


def find_most_constrained(puzzle: List[List[str]], non_assigned: List[List[int]]) -> int:
    curr_most_constrained = (-1, -1)
    light_map_up(puzzle)

    for cell in non_assigned:
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