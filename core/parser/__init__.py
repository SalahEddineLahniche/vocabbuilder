#takes a file with the format of
#word;choice1.correct choice2=.choice3
##section
#word;choice1.correct choice2=.choice3
#and transforme it to a file kind of list id;word
#the first line of the distination folder is a number 

def parse(path, destination):
	f = open(path)
	g = open(destination, "r")
	tmpFile = open("tmp", "w")

	i = int(g.readline()[:-1])
	i += 1

	line = g.readline()
	while line != "":
		tmpFile.write(line)
		line = g.readline()

	g.close()
	tmpFile.close()

	g = open(destination, "w")
	tmpFile = open("tmp", "r")
	dico = []
	tmpLine = f.readline()[:-1]
	tmpArray = []
	j = 0
	while tmpLine:
		if(tmpLine[0] == "#"):
			tmpLine = f.readline()[:-1]
			continue
		tmpArray = tmpLine.split(";")
		dico.append([tmpArray[1].split("."), tmpArray[0]])
		j +=  1 + len(dico[-1][0])
		tmpLine = f.readline()[:-1]

	g.write(str(i + j - 1) + "\n")

	line = tmpFile.readline()
	while line != "":
		g.write(line)
		line = tmpFile.readline()

	# g.write("\n")
	for key in dico:
		g.write(str(i) + ";" + key[1] + "\n")
		i += 1
		for word in key[0]:
			if word[-1] == "=":
				word = word[:-1]
			g.write(str(i) + ";" + word + "\n")
			i += 1

	f.close()
	g.close()
	tmpFile.close()


		