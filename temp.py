

short_rules = []
long_rules = []

textfile = open("etc/sudoku-rules-9x9-rev.txt", "w")
for line in open("etc/sudoku-rules-9x9.txt", "r"):
    if line[0] == 'p': textfile.write(line)
    elif len(line) <= 12:
        short_rules.append(line)
    else:
        long_rules.append(line)




for element in short_rules:
    textfile.write(element)
for element in long_rules:
    textfile.write(element)

textfile.close()