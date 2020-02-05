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