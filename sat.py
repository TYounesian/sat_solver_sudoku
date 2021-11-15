
# SAT Solver for Sudoku

# Read the DIMACS files
import pdb
with open('sudoku-rules.txt') as f:
    lines = f.readlines()

with open('sudoku-example.txt') as f:
    game_lines = f.readlines()

num_var1 = int(lines[0][6])
num_var2 = int(lines[0][7])
num_var3 = int(lines[0][8])

#total_var_num = num_var1 * num_var2 * num_var3 #9*9*9

var_list = [[[None for __ in range(num_var1)] for _ in range (num_var2)] for ___ in range (num_var3)]# a list of 9*9*9 variables

print ("general rules length:", len(lines[1]))

# Initiate all the clauses as None per line. Later we will add the literals and "or" them
clauses_list = [None for _ in range (len(lines) - 1 + len(game_lines))]


for i in range (1, len(lines)):
	inside_lines = []
	lines_sep = []

	# split each line (clause) into its literals
	inside_lines = lines[i].split() # these are values like '111'
	clause_len = len(inside_lines) # number of literals in that clause


	clauses_list [i - 1] = var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1] if \
	 int(inside_lines[0])>0 else not(var_list[int(inside_lines[0][1])-1][int(inside_lines[0][2])-1][int(inside_lines[0][3])-1]) # assign the first literal to the clause

	
	for j in range (1, clause_len-1): 
		
		literal = var_list[int(inside_lines[j][0])-1][int(inside_lines[j][1])-1][int(inside_lines[j][2])-1] if \
		 int(inside_lines[j])>0 else not(var_list[int(inside_lines[j][1])-1][int(inside_lines[j][2])-1][int(inside_lines[j][3])-1])
		clauses_list [i - 1] = clauses_list [i - 1] or literal


for i in range (0, len(game_lines)):
	inside_lines = game_lines[i].split()
	print(game_lines[i])
	var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1] = True
	clauses_list [len(lines) + i - 1] = var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1]















