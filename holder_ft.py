# This guy uses a lot of stuff from backtracking.py

from makePuzzles import *
from backtracking import *
import time
import random

countNodes = 0


# prioritize_bulbs
def markBulbStuff(puz,i,j):
    rows = len(puz)
    cols = len(puz[0])
    # mark up
    k=i-1
    while k>=0 and isinstance( puz[k][j], int ):
        puz[k][j]=puz[k][j]%2
        k-=1

    # mark down
    k=i+1
    while k<len(puz)-1 and isinstance( puz[k][j], int ):
        puz[k][j]=puz[k][j]%2
        k+=1

    # mark left
    k=j-1
    while k>=0 and isinstance( puz[i][k], int ):
        puz[i][k]=puz[i][k]%2
        k-=1

    # mark right
    k=j+1
    while k<len(puz[0])-1 and isinstance( puz[i][k], int ):
        puz[i][k]=puz[i][k]%2
        k+=1

def checkEdgeCorner(puz,i,j):
    # not an edge or corner status = 0
    # an edge, status = 1
    # a corner status = 2
    status = 0
    if(i==0 or i==len(puz)-1):
        status+=1
    if(j==0 or j==len(puz[0])-1):
        status+=1

    return status

def numPotentialAdjacent(puz, i, j):
	rows = len(puz)
	cols = len(puz[0])
	count = 0
	if i > 0 and isinstance( puz[i-1][j], int ) and puz[i-1][j] >= 2:
		count += 1
	if i < rows-1 and isinstance( puz[i+1][j], int ) and puz[i+1][j] >= 2:
		count += 1
	if j > 0 and isinstance( puz[i][j-1], int ) and puz[i][j-1] >= 2:
		count += 1
	if j < cols-1 and isinstance( puz[i][j+1], int ) and puz[i][j+1] >= 2:
		count += 1
	return count

# prioritize_walls
def markWallStuff(puz,i,j):
    rows = len(puz)
    cols = len(puz[0])
    k=i-1
    if i > 0 and isinstance( puz[k][j], int ):
        puz[k][j] = int(puz[k][j]/2)*2
        if puz[k][j] == 2:
            markBulbStuff(puz,k,j)

    k=i+1
    if i < rows-1 and isinstance( puz[k][j], int ):
        puz[k][j] = int(puz[k][j]/2)*2
        if puz[k][j] == 2:
            markBulbStuff(puz,k,j)

    k=j-1
    if j > 0 and isinstance( puz[i][k], int ):
        puz[i][k] = int(puz[i][k]/2)*2
        if puz[i][k] == 2:
            markBulbStuff(puz,i,k)

    k=j+1
    if j < cols-1 and isinstance( puz[i][k], int ):
        puz[i][k] = int(puz[i][k]/2)*2
        if puz[i][k] == 2:
            markBulbStuff(puz,i,k)


# check_curr_state
def checkPuzzle(puz,notassigned):
    rows = len(puz)
    cols = len(puz[0])

    # Mark all the unassigned spots on the puzzle
    # 3 marks the spot can be either 'b' or '_'
    for i in range(rows):
        for j in range(cols):
            key = rows*i+j
            if key in notassigned:
                puz[i][j] = 3

    # Mark all bulbs
    # if the spot cannot be a bulb, make it an integer 1
    for i in range(rows):
        for j in range(cols):
            if puz[i][j] == 'b':
                markBulbStuff(puz,i,j)


    # Mark all walls
    # if the spot cannot be a '_' and can be a 'b' then mark spot as 2
    # if the spot cannot be either, mark spot as 0
    wallNums = ['0','1','2','3','4']
    for i in range(rows):
        for j in range(cols):
            if puz[i][j] in wallNums:
                # the integer value of the wall
                wallVal = int(puz[i][j])

                # the number of adjacent bulbs to the wall
                adjBulbs = numAdjacent(puz,i,j)

                # the number of potential bulbs adjacent to the wall
                adjPotentialBulbs = numPotentialAdjacent(puz,i,j)

                # not an edge or corner status = 0
                # an edge, status = 1
                # a corner status = 2
                status = checkEdgeCorner(puz,i,j)

                numRequiredBulbs = wallVal - adjBulbs - status

                #if adjPotentialBulbs == numRequiredBulbs:
                #    markWallStuff(puz,i,j)

    # Figure out the return value and reset puzzle back to normal
    ret = True
    for i in range(rows):
        for j in range(cols):
            if isinstance( puz[i][j], int ):
                if puz[i][j] == 0:
                    ret = False
                puz[i][j] = '_'

    return ret


# forward_checking
def forwardchecking(puz, domain, notassigned,heuristic):
    global countNodes
    countNodes+=1
    if countNodes%10000 == 0:
        print(countNodes,end='\r')
    if countNodes == 5000000:
        return 'timeout'
    if complete(puz):
        return puz
    if len(notassigned)== 0 or not checkPuzzle(puz,notassigned):
        return "back"
    val = getFromHeuristic(puz,notassigned,heuristic)
    i = val[0]
    j = val[1]

    for value in domain:
        puz[i][j] = value
        if ((value != "_" and legal(puz,i,j)) or value == "_"):
            result = forwardchecking(puz, domain, notassigned,heuristic)
            if result != "back":
                return result

    notassigned.append(val)
    return "back"

def solve(puz,heuristic):
	domain = ("b", "_")
	notassigned = getBlanks(puz)
	return forwardchecking(puz, domain, notassigned,heuristic)

def main( argv = None ):
    if (argv == None ):
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='create a modified Akari Puzzle')
    parser.add_argument('--width', action='store', dest='width', type=int, default=8)
    parser.add_argument('--height', action='store', dest='height', type=int, default=8)
    parser.add_argument('--verbose', '-v', action='count', dest='verbose', default=0)
    parser.add_argument('--count', '-c', action='store', dest='count', default=1)
    parser.add_argument('--solution', '-s', action='store_true', dest='solution', default=False)
    parser.add_argument('--bulbs', '-b', action='store', dest='bulbs', type=int, default=-1)
    parser.add_argument('--walls', '-w', action='store', dest='walls', type=int, default=-1)
    parser.add_argument('--debug', action='store', dest='debug', type=str, default="none")
    parser.add_argument('--heuristic', action='store', dest='heuristic', type=str, default="constrained")
    parser.add_argument('--input', action='store', dest='input', type=str, default="")


    args = parser.parse_args( argv )
    if (args.verbose > 0 ):
        print('AkariMaker {0}x{1} bulbs {2} walls {3}'.format(args.width, args.height, args.bulbs, args.walls ))

    if args.input == '':
        puzzle = makePuzzles(args.count, args.width, args.height, args.bulbs, args.walls, args.solution )

        clearSolution(puzzle)

    else:
        puzzle = getTextInput(args.input)

    debug = args.debug
    print()

    start = time.time()
    solution = solve(puzzle,args.heuristic)
    end = time.time()

    if solution == 'timeout':
        print("Timeout!\nTime taken %f seconds" % (end-start))
    else:
        printPuzzle(solution)
        print("Time taken %f seconds\n" % (end-start))

    print("Nodes visited: %d\n" % (countNodes))



if __name__ == '__main__':
    main()
