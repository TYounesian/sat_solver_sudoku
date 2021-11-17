import itertools
from copy import deepcopy

rules = "etc/sudoku-rules-9x9.txt"
sudokuSource = "etc/damnhard.sdk.txt"
solution = []

def getRules(rulePath):
    rules = [line[:-3].split(' ') for line in open(rulePath, "r")][1:]
    return [[int(x) for x in clause] for clause in rules]

def getSudokuFromFile(sudokuPath):
    sudokus = [line[:-1] for line in open(sudokuPath, "r")] # Read in the sudokus from a file
    gridsize = int(len(sudokus[0])**0.5)
    cnfs = []
    for sudoku in sudokus:
        clause = []
        for place in range(len(sudoku)):
            if sudoku[place] != '.':
                clause.append([int(str(place//gridsize + 1) + str(place % gridsize + 1) + str(sudoku[place]))])
        cnfs.append(clause)
    return cnfs


def dpll(cnf, branch=[]):
    while True:
        unitClauses = list(set([c[0] for c in cnf if len(c) == 1]))
        if not branch: solution.extend(unitClauses)
        if not unitClauses: break
        for p in unitClauses: trimming(p, cnf)
    if not cnf: return True  # If the set is empty we satisfied it all
    if not all(cnf): return False  # If a clause is empty it cannot be satisfied
    p = heuristics_DLCS(cnf)
    if dpll(deepcopy(cnf) + [[p]], branch + [p]):
        solution.append(p)
        return solution
    elif dpll(deepcopy(cnf) + [[-p]], branch + [-p]):
        solution.append(-p)
        return solution
    else: return False


def trimming(p, c):
    for clause in c[:]:
        if p in clause: c.remove(clause)
        elif -p in clause: c[c.index(clause)].remove(-p)


def heuristics_DLCS(cnf_heur):
    flat_cnf = [abs(p) for c in cnf_heur for p in c]  # Flatten the cnf and no distinction between positive and negative
    return max(flat_cnf, key=flat_cnf.count)  # Return the most frequent predicate


def solver_complete(cnf):
    cnfLoop = cnf[:]
    for clause in cnfLoop:
        for a, b in itertools.combinations(clause, 2):
            if (a + b) == 0: cnf.remove(clause)
    return dpll(cnf)


r = getRules(rules)
puzzle = getSudokuFromFile(sudokuSource)[1]
r = r + puzzle
# m = list(set([p for c in r for p in c]))
# m.sort()
# print(m)

solutions = solver_complete(r)
print("**********************")
print(solutions.sort())
only_numbers = [x for x in solutions if x >= 0]

print("================")
print("Solution: ", solutions)
print(len(solution))
print("Puzzle: ", puzzle)
print("Solution: ", only_numbers)
print(len(only_numbers))
