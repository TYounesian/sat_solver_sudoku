import itertools
from copy import deepcopy
import time
import sys
import random

# =================================== SETUP - READING FILES ===================================

def getRules(rulePath):
    return [line[:-3].split(' ') for line in open(rulePath, "r")][1:]               # Returns the clauses as lists of integers


def getSudokuFromFile(sudokuPath):
    sudokus = [line[:-1] for line in open(sudokuPath, "r")]     # Read in the sudokus from a file
    gridsize = int(len(sudokus[0])**0.5)                        # Dynamically determine grid size based on len(line)
    c16 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
    cnfs = []
    for sudoku in sudokus:
        clause = []
        for place in range(len(sudoku)):                    # Number format is changed to CNF
            if sudoku[place] != '.':                        # Calculates the place of the number based on the index
                clause.append([c16[place//gridsize] + c16[place % gridsize] + str(sudoku[place])])
        cnfs.append(clause)
    return cnfs

# =================================== DPLL Algorithm ===================================

def dpll(cnf, heuristic):
    global branches, heur_solution
    cls = []                                                            # Collects the unit clauses from each iter.
    while True:
        unitClauses = list(set([c[0] for c in cnf if len(c) == 1]))     # Unit clauses are clauses with lenght of 1
        #print(cls)
        if not unitClauses: break                                       # Quit if there are no more unit clauses
        cls.extend([x for x in unitClauses if x[0] != '-'])                   # Save only the positive predicates
        for p in unitClauses:
            for clause in cnf[:]:
                if p in clause: cnf.remove(clause)                      # Delete the clause with the predicate
                elif neg(p) in clause: cnf[cnf.index(clause)].remove(neg(p))    # Delete the negative of predicate from clause
    heur_solution.extend(list(set(cls)))
    #print(len(heur_solution), heur_solution)
    if not cnf:
        solution.extend(list(set(cls)))                 # If the set is empty we satisfied it all
        return list(set(solution))                      # And the unit clauses can be added to the solution
    if not all(cnf):
        heur_solution = list(set(heur_solution) - set(cls))
        return False                       # If a clause is empty it cannot be satisfied
    p = heuristic(cnf)                                  # Choose a heuristic
    branches += 1                                       # Either branch should be correct
    if dpll(deepcopy(cnf) + [[p]], heuristic) or dpll(deepcopy(cnf) + [[neg(p)]], heuristic):
        solution.extend(list(set(cls)))                                 # Add the solution to the set
        return list(set(solution))                                      # Return solutions
    else: return False


def neg(x):
    if x[0] == "-": return x[1:]
    else: return "-" + x

def solver_complete(cnf, heuristic):
    # cnfloop = cnf[:]                                    # ------------- Needs checking for tautologies -------------
    # for clause in cnfloop:                              # Looping trough a copy of the input and
    #     for a, b in itertools.combinations(clause, 2):  # checking if any of the paris in the clauses sum to 0
    #         if (a + b) == 0: cnf.remove(clause)         # ----------------------------------------------------------
    return dpll(cnf, heuristic)                                    # ------- Beginning real algorithm


# =================================== Heuristics ===================================

def heuristics_HUMAN(cnf):
    """
    Looks for clauses with the most filled out rows and columns
    """
    global heur_solution
    #
    rows = {}
    cols = {}
    cubes = {}
    for literal in heur_solution:
        if literal[0] in rows: rows[literal[0]]+= 1
        else: rows[literal[0]] = 1
        if literal[1] in cols: cols[literal[1]]+= 1
        else: cols[literal[1]] = 1
    max(rows, key=rows.get)
    max(cols, key=cols.get)

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


def heuristics_DLCS(cnf):                               # Dynamic Largest Combined Sum
    flat_cnf = [abs(p) for c in cnf for p in c]         # Flatten the cnf
    return max(flat_cnf, key=flat_cnf.count)            # Return the most frequent predicate


def heuristics_FIRST(cnf):                              # First predicate we encounter
    return cnf[0][0]                                    # Return the first predicate from the first clause


def heuristics_RAND(cnf):                               # Returns a random predicate
    rc = random.randrange(0, len(cnf))                  # Random clause
    rp = random.randrange(0, len(cnf[rc]))                  # Random predicate
    return cnf[rc][rp]                                    # Return the first predicate from the first clause

def heuristics_DLCS_2(cnf):
    weights = {}
    for clause in cnf:
        for literal in clause:
            if literal in weights:
                weights[literal] += 1
            else:
                weights[literal] = 1
    return max(weights, key=weights.get)            # Return the most frequent predicate


heuristics = {
    'HUMAN' : heuristics_HUMAN,
    'JWOS': heuristics_JWOS,
    'JWTS': heuristics_JWTS,
    'DLCS': heuristics_DLCS,
    'DLCS_2': heuristics_DLCS_2,
    'FIRST': heuristics_FIRST,
    'RAND' : heuristics_RAND
}

#  =================================== MAIN PROGRAM ===================================

if __name__ == '__main__':


    # --------------- 16 x 16 ---------------
    # rules = "etc/sudoku-rules-16x16.txt"
    # sudokuSource = "etc/16x16.txt"

    # ---------------- 9 x 9 ----------------
    rules = "etc/sudoku-rules-9x9.txt"
    sudokuSource = "etc/damnhard.sdk.txt"
    # sudokuSource = "etc/1000 sudokus.txt"

    # ---------------- 4 x 4 ----------------
    # rules = "etc/sudoku-rules-4x4.txt"
    # sudokuSource = "etc/4x4.txt"

    branches = 0
    totaltime = 0
    totalbranches = 0

    if len(sys.argv) > 1:
        try:
            heuristic = heuristics[sys.argv[1]]
        except:
            sys.exit("ERROR: '{}' Not valid heuristic.".format(sys.argv[1]) +
                     "\nValid heuristics: {}".format(heuristics.keys()))
    else: heuristic = heuristics['RAND']

    puzzles = getSudokuFromFile(sudokuSource)
    loops = 1
    totalsolutions = 0
    for i in range(loops):
        solution = []
        heur_solution = []
        puzzle = puzzles[i]
        start = time.time()
        solutions = solver_complete(getRules(rules) + puzzle, heuristic)
        timetaken = time.time() - start
        totaltime += timetaken
        totalbranches += branches
        if solutions: totalsolutions += len(solutions)
        else:
            print("No solution to puzzle: {}".format(puzzle))
            break
        #  =================================== SOLUTION CHECK ==================================
        print("\n====== Puzzle No. {} ======\n".format(i))
        print("Puzzle: ", puzzle)
        print("Solution: ", solutions)
        print("Number of solutions", len(solutions))
        print("Branching needed: ", branches)
        print("Time taken", timetaken)
    print("\n{}\nAvg time: {}\nAvg branches: {}".format("=" * 100, totaltime / loops, totalbranches / loops))
    print(totalsolutions / loops)