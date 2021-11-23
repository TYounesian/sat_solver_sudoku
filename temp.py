

# short_rules = []
# # long_rules = []
# #
# # textfile = open("etc/sudoku-rules-9x9-rev.txt", "w")
# # for line in open("etc/sudoku-rules-9x9.txt", "r"):
# #     if line[0] == 'p': textfile.write(line)
# #     elif len(line) <= 12:
# #         short_rules.append(line)
# #     else:
# #         long_rules.append(line)
# #
# #
# #
# #
# # for element in short_rules:
# #     textfile.write(element)
# # for element in long_rules:
# #     textfile.write(element)
# #
# # textfile.close()

rules = []
c16 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
textfile = open("etc/sudoku-rules-16x16-rewrote.txt", "w")
for line in open("etc/sudoku-rules-16x16.txt", "r"):
    if line[0] == 'p': textfile.write(line)
    else:
        clause = line[:-3].split(" ")
        newclause = []
        for c in clause:
            neg = ""
            if int(c) < 0: neg = "-"
            nf = neg + c16[abs(int(c)) // 17**2] + c16[abs(int(c)) % 17**2 // 17] + c16[abs(int(c) % 17**2) % 17]
            print(c, nf, str(abs(int(c)) // 17**2) + str(abs(int(c)) % 17**2 // 17) + str(abs(int(c) % 17**2) % 17))
            newclause.append(nf)
        rules.append(newclause)

textfile.close()