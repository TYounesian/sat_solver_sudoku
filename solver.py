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


def dpll(cnf):
    cls = []
    while True:
        unitClauses = list(set([c[0] for c in cnf if len(c) == 1]))
        if not unitClauses: break
        cls.extend(unitClauses)
        for p in unitClauses: trimming(p, cnf)
    if not cnf:
        solution.extend(list(set(cls)))
        return list(set(solution))  # If the set is empty we satisfied it all
    if not all(cnf): return False  # If a clause is empty it cannot be satisfied
    p = heuristics_DLCS(cnf)
    if dpll(deepcopy(cnf) + [[p]]) or dpll(deepcopy(cnf) + [[-p]]):
        solution.extend(list(set(cls)))
        return list(set(solution))
    else: return False


def trimming(p, c):
    for clause in c[:]:
        if p in clause: c.remove(clause)
        elif -p in clause: c[c.index(clause)].remove(-p)


def heuristics_DLCS(cnf_heur):
    flat_cnf = [abs(p) for c in cnf_heur for p in c]  # Flatten the cnf and no distinction between positive and negative
    return max(flat_cnf, key=flat_cnf.count)  # Return the most frequent predicate


def solver_complete(cnf):
    cnfLoop = cnf[:]                                    # ------------- Needs checking for tautologies -------------
    for clause in cnfLoop:                              # Looping trough a copy of the input and
        for a, b in itertools.combinations(clause, 2):  # checking if any of the paris in the clauses sum to 0
            if (a + b) == 0: cnf.remove(clause)         # ----------------------------------------------------------
    return dpll(cnf)                                    # ------- Beginning real algorithm


r = getRules(rules)
puzzle = getSudokuFromFile(sudokuSource)[1]
r = r + puzzle

solutions = solver_complete(r)
print("**********************")
print(solutions)
positives = [x for x in solutions if x >= 0]

print("================")
print("Solution: ", solutions)
print(len(solutions))
print("Puzzle: ", puzzle)
print("Solution: ", positives)
print(len(positives))
