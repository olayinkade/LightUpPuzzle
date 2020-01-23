from typing import List


def check_edge_corner(puzzle: List[List[int]], r: int, c: int) -> int:
    status = 0
    if r == 0 or r == len(puzzle) - 1:  # edge
        status += 1
    if c == 0 or c == len(puzzle[0]) - 1:  # edge, status = 2 if it's a corner
        status += 1
    return status


def get_total_potential_adjacent(puzzle: List[List[int]], r: int, c: int):
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


