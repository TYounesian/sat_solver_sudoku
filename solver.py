import itertools
from copy import deepcopy
import time



rules = "etc/sudoku-rules-9x9.txt"
sudokuSource = "etc/damnhard.sdk.txt"
#sudokuSource = "etc/1000 sudokus.txt"

branches = 0
# =================================== SETUP - READING FILES ===================================

def getRules(rulePath):
    rules = [line[:-3].split(' ') for line in open(rulePath, "r")][1:]  # Counts from the 3rd line
    return [[int(x) for x in clause] for clause in rules]               # Returns the clauses as lists of integers


def getSudokuFromFile(sudokuPath):
    sudokus = [line[:-1] for line in open(sudokuPath, "r")]     # Read in the sudokus from a file
    gridsize = int(len(sudokus[0])**0.5)                        # Dynamically determine grid size based on len(line)
    cnfs = []
    for sudoku in sudokus:
        clause = []
        for place in range(len(sudoku)):                    # Number format is changed to CNF
            if sudoku[place] != '.':                        # Calculates the place of the number based on the index
                clause.append([int(str(place//gridsize + 1) + str(place % gridsize + 1) + str(sudoku[place]))])
        cnfs.append(clause)
    return cnfs

# =================================== DPLL Algorithm ===================================

def dpll(cnf):
    global branches
    cls = []                                                            # Collects the unit clauses from each iter.
    while True:
        unitClauses = list(set([c[0] for c in cnf if len(c) == 1]))     # Unit clauses are clauses with lenght of 1
        if not unitClauses: break                                       # Quit if there are no more unit clauses
        cls.extend([x for x in unitClauses if x > 0])                   # Save only the positive predicates
        for p in unitClauses:
            for clause in cnf[:]:
                if p in clause: cnf.remove(clause)                      # Delete the clause with the predicate
                elif -p in clause: cnf[cnf.index(clause)].remove(-p)    # Delete the negative of predicate from clause
    if not cnf:
        solution.extend(list(set(cls)))                 # If the set is empty we satisfied it all
        return list(set(solution))                      # And the unit clauses can be added to the solution
    if not all(cnf): return False                       # If a clause is empty it cannot be satisfied
    p = heuristics_JWOS(cnf)                            # Choose a heuristic
    branches += 1
    if dpll(deepcopy(cnf) + [[p]]) or dpll(deepcopy(cnf) + [[-p]]):     # Either branch should be correct
        solution.extend(list(set(cls)))                                 # Add the solution to the set
        return list(set(solution))                                      # Return solutions
    else: return False


def heuristics_JWOS(cnf):                               # One-sided Jeroslow-Wang Heuristics
    weights = {}
    for clause in cnf:
        for literal in clause:
            if literal in weights: weights[literal] += 2 ** -len(clause)
            else: weights[literal] = 2 ** -len(clause)
    return max(weights, key=weights.get)                # Return the most frequent predicate


def heuristics_JWTS(cnf):                               # Two-sided Jeroslow-Wang Heuristics
    weights = {}
    for clause in cnf:
        for literal in clause:
            literal = abs(literal)
            if literal in weights: weights[literal] += 2 ** -len(clause)
            else: weights[literal] = 2 ** -len(clause)
    return max(weights, key=weights.get)                # Return the most frequent predicate



def heuristics_DLCS(cnf):
    flat_cnf = [abs(p) for c in cnf for p in c]    # Flatten the cnf
    return max(flat_cnf, key=flat_cnf.count)            # Return the most frequent predicate


def heuristics_DLCS_2(cnf):
    weights = {}
    for clause in cnf:
        for literal in clause:
            if literal in weights:
                weights[literal] += 1
            else:
                weights[literal] = 1
    return max(weights, key=weights.get)            # Return the most frequent predicate


def solver_complete(cnf):
    cnfloop = cnf[:]                                    # ------------- Needs checking for tautologies -------------
    for clause in cnfloop:                              # Looping trough a copy of the input and
        for a, b in itertools.combinations(clause, 2):  # checking if any of the paris in the clauses sum to 0
            if (a + b) == 0: cnf.remove(clause)         # ----------------------------------------------------------
    return dpll(cnf)                                    # ------- Beginning real algorithm


heuristics = {
    'JWOS': heuristics_JWOS,
    'JWTS': heuristics_JWTS,
    'DLCS': heuristics_DLCS,
    'DLCS_2': heuristics_DLCS_2,
}

#  =================================== MAIN PROGRAM ===================================
totaltime = 0
totalbranches = 0

puzzles = getSudokuFromFile(sudokuSource)
loops = 10
totalsolutions = 0
for i in range(loops):
    solution = []
    puzzle = puzzles[i]
    start = time.time()
    solutions = solver_complete(getRules(rules) + puzzle)
    timetaken = time.time() - start
    totaltime += timetaken
    totalbranches += branches
    totalsolutions += len(solutions)
    #  =================================== SOLUTION CHECK ==================================
    print("\n====== Puzzle No. {} ======\n".format(i))
    print("Puzzle: ", puzzle)
    print("Solution: ", solutions)
    print("Number of solutions", len(solutions))
    print("Branching needed: ", branches)
    print("Time taken", timetaken)
print("*"*100)
print("Average time taken: {}\nAverage branches needed: {}".format(totaltime/loops, totalbranches/loops))
print(totalsolutions/loops)