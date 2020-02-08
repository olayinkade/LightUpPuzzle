# LightUpPuzzle
Using various search algorithms to find solutions to the light up puzzle problem

## How to run the program:
*Python 3 is required*

**Run forward checking algorithm**: python forward_checking.py --heuristic heuristic_name

where 'heuristic_name' could be either 'most_constrained', 'most_constraining' or 'hybrid'

**Run backtracking algorithm**: python backtrack.py --heuristic heuristic_name

where 'heuristic_name' could be either 'most_constrained', 'most_constraining' or 'hybrid'

**Change the puzzle:** Open the input text file **puzzle.txt**, and paste the puzzle together with its size (as the requirement) there, sae and run the program.


*After converting the problem to a CSP problem, we have:*
- Variables: empty/potential cells that can be bulbs
- Domain: "_" for empty cells, "b" for bulbs
- Constraints: for this problem, we use the following as constraints:
  + Position of the cell: in the middle, in the corner, on the edge or stuck between walls. These can all affect the likelihood if a cell can be a bulb.
  + Nunber of walls around a cell: if a cell is surrounded by walls, especially the ones with higher number like 3 or 4, it's more likely to be a bulb, hence, more constrained.
  + Number of lit up cells around: the number of lit up neighbours, this can affect the likelihood of a cell being a bulb too.
  
## PREPROCESSING AND HEURISTICS:
**Preprocessing**: in order to limit the number of potential variables, we do a quick check through all walls, to see if any neighbouring cells of a wall must be bulbs. For example, 4 cells surrounding a wall 4 must be bulbs, or 3 neighbouring cells surrounding a wall 3 on the edge, or 2 cells surrounding a wall 2 in the edge. More generally, if the number of empty neighbours of a wall is the same as the number of required bulbs surrounding that wall, we will place bulbs there and light up all corresponding cells, through that we can eliminate a significant amount of potential variables in a typical puzzle.
<br><br>We remove all the empty cell surrounding a zero wall
<br><br>All walls that has a valid number of bulbs If there are other empty cells surrounding i remove those empty cells from the list of possible places I can put a bulb

**Heuristics**:
- *Most constrained*: the constraint of each variable (i.e. cell) is the sum of all three types of constraints listed above.
- *Most constraining*: we choose the to place a bulb in a cell that can light up the largest number of corresponding cells. This means that the cell with the highest impact will be chosen.
- *Hybrid*: the combination of most constrained and most constraining heuristic. The algorithm will run most constrained first, and if most constrained return a list of cells that have the same amount of constraint, it will use most constraining to break the tie.

## ALGORITHMS:
**Forward checking**: The algorithm checks the variables and sees if a cell cannot be either empty ('_') or ('b'), then it backtracks. This basically follows the standard algorithm shown in class.

**Backtracking**: This algorithm uses DFS to search for the optimal position to bulbs to fulfill all constrains
