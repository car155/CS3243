# CS3243 Introduction to Artificial Intelligence
# Project 2
# G65: Carissa Ying Geok Teng, Ernest Lian Qi Quan

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class State:
    def __init__(self, assigned, unassigned):
        self.assigned = assigned
        unassigned.sort(key=self.sortByDomainSize)
        self.unassigned = unassigned

    def sortByDomainSize(self, x):
        return len(x.domain)


class Cell:
    def __init__(self, cellID, domain):
        self.domain = domain
        self.cellID = cellID

    def remove(self, value):
        self.domain = self.domain - set([value])

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, state):
        self.stack.append(state)
    
    def pop(self):
        return self.stack.pop()

    def notEmpty(self):
        return len(self.stack) > 0


def initStartState(puzzle, coordMapper):
    unassigned = []
    assigned = {}
    cellID = 1

    for i in range(9):
        for j in range(9):

            val = puzzle[i][j]
            if val != 0: # starts with a value
                assigned[cellID] = val
            else: 
                domain = set(range(1, 10)) # needs to be filled
                unassigned.append(Cell(cellID, domain))

            coordMapper[cellID] = (i, j, (i // 3) * 3 + (j // 3))
            cellID += 1

    return initDomain(assigned, unassigned, coordMapper)


def initDomain(assigned, unassigned, coordMapper):
    for var in assigned:
        row, col, square = coordMapper[var]

        for unassignedVar in unassigned:
            unRow, unCol, unSquare = coordMapper[unassignedVar.cellID]

            if (row == unRow # same row
                    or col == unCol # same col
                    or square == unSquare): # same square
                unassignedVar.remove(assigned[var]) # constraints

    return State(assigned, unassigned)


def forwardCheck(assigned, assignedVal, unassigned, coordMapper):
    newUnassigned = []
    newAssigned = assigned.copy()

    var = unassigned[0].cellID # varQueue.pop()
    newAssigned[var] = assignedVal # assign
    row, col, square = coordMapper[var]

    for x in unassigned[1:]: # for remaining variables, x
        unRow, unCol, unSquare = coordMapper[x.cellID]

        if (row == unRow # in Vars(C)
                or col == unCol
                or square == unSquare):

            # check if other unassigned variables only have 1 option that clashes with current assignment
            if len(x.domain) == 1 and assignedVal in x.domain:
                return False
            else:
                newUnassigned.append(Cell(x.cellID, x.domain - set([assignedVal])))

        else:
            newUnassigned.append(x)

    return State(newAssigned, newUnassigned)

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.state = None

    def solve(self):
        # TODO: Write your code here
        # set up 
        coordMapper = {}
        stack = Stack()
        stack.push(initStartState(self.puzzle, coordMapper))

        while stack.notEmpty():
            state = stack.pop()

            if len(state.unassigned) > 0:
                validDomainValues = state.unassigned[0].domain # order domain values
                for v in validDomainValues:
                    result = forwardCheck(state.assigned, v, state.unassigned, coordMapper)
                    if result != False:
                        stack.push(result)
            else:
                # no unassigned left to perform assignment
                break
        if state is not None :
            for var in state.assigned:
                row, col, square = coordMapper[var]
                self.ans[row][col] = state.assigned[var]
        # self.ans is a list of lists
        return self.ans
    

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
