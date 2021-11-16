
# SAT Solver for Sudoku

# Read the DIMACS files
import pdb


def idx_invertor(idx):
	divisor = idx // 9
	remainder = idx % 9
	if divisor > 8:
		second_divisor = divisor // 9
		i = second_divisor
		j = divisor
		k = remainder
	elif divisor > 0:
		i = 0
		j = divisor
		k = remainder
	else:
		i = 0
		j = divisor
		k = remainder

	return i, j ,k


class sudoku():


	def __init__ (self, lines, game_lines):
		self.lines = lines
		self.game_lines = game_lines


	def read_lines(self):
		num_var1 = int(self.lines[0][6])
		num_var2 = int(self.lines[0][7])
		num_var3 = int(self.lines[0][8])
		#total_var_num = num_var1 * num_var2 * num_var3 #9*9*9

		self.var_list = [[[None for __ in range(num_var1)] for _ in range (num_var2)] for ___ in range (num_var3)] # a list of 9*9*9 variables


		print ("general rules length:", len(self.lines[1]))

		# Initiate all the clauses as None per line. Later we will add the literals and "or" them
		self.clauses_list = [None for _ in range (len(self.lines) - 1 + len(self.game_lines))]
		self.clauses_bool = [None for _ in range (len(self.lines) - 1 + len(self.game_lines))]
		self.clauses_size = [None for _ in range (len(self.lines) - 1 + len(self.game_lines))]
		self.clauses_dict = {"list": self.clauses_list, "bool": self.clauses_bool, "size": self.clauses_size}

		for i in range (1, len(self.lines)):
			inside_lines = []
			lines_sep = []

			# split each line (clause) into its literals
			inside_lines = self.lines[i].split() # these are values like '111'
			clause_len = len(inside_lines) # number of literals in that clause

			self.clauses_list [i - 1] = inside_lines
			self.clauses_bool [i - 1] = self.var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1] if \
			 int(inside_lines[0])>0 else not(self.var_list[int(inside_lines[0][1])-1][int(inside_lines[0][2])-1][int(inside_lines[0][3])-1]) # assign the first literal to the clause
			self.clauses_size[i - 1] = clause_len
			
			for j in range (1, clause_len-1): 
				
				literal = self.var_list[int(inside_lines[j][0])-1][int(inside_lines[j][1])-1][int(inside_lines[j][2])-1] if \
				 int(inside_lines[j])>0 else not(self.var_list[int(inside_lines[j][1])-1][int(inside_lines[j][2])-1][int(inside_lines[j][3])-1])
				self.clauses_bool [i - 1] = self.clauses_bool [i - 1] or literal


		for i in range (0, len(game_lines)):
			inside_lines = self.game_lines[i].split()
			self.clauses_list = inside_lines

			print(self.game_lines[i])
			self.var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1] = True
			self.clauses_bool [len(self.lines) + i - 1] = self.var_list[int(inside_lines[0][0])-1][int(inside_lines[0][1])-1][int(inside_lines[0][2])-1]
			self.clauses_size[len(self.lines) + i - 1] = 1

		return self.clauses_list, self.clauses_bool, self.clauses_size, self.var_list

	def unit_prop (self, l): 
	#set unit clauses to True, remove those clauses and remove the negation of that literal
		if l > 0: 
			l = True
			for i in range (0, len(self.clauses_list)):
				if any(self.clauses_list[i]) == l
					if self.clauses_size == 1
						# remove that clause
					else:
						#remove the negation of that literal
		else:
			l = False
			for i in range (0, len(self.clauses_list)):
				if any(self.clauses_list[i]) == l
					if self.clauses_size == 1
						# remove that clause
					else:
						#remove the negation of that literal

		return self

#################### ************** Start DP ******************#####################
	def dpll(self):
		if all(self.clauses_size) == 1:
			return True
		elif any(self.clauses_size) == 0:
			return False
		else: # unit clause propagation
			for i in range (0, len(self.clauses_bool)):
				# do unit_prop
			for i in range (0, len(self.clauses_bool)):
				#pure literal assign
			


			

with open('sudoku-rules.txt') as f:
	lines = f.readlines()

with open('sudoku-example.txt') as f:
	game_lines = f.readlines()

lines = sudoku(lines, game_lines)
clauses_list, clauses_bool, clauses_size, var_list = lines.read_lines()























