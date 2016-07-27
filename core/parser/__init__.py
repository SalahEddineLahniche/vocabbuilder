#takes a file with the format of
#word;choice1.correct choice2=.choice3
##section
#word;choice1.correct choice2=.choice3
#and transforme it to a file kind of list id;word

import os.path
import os

def parse(path, destination):
	try:
		# check whether the files exists & init them
		if not os.path.isfile(path):
			return -1
		if not os.path.isfile(destination):
			g = open(destination, "w")
			g.write("0")
			g.close()
		# end
		# open the files
		f = open(path)
		g = open(destination, "r")
		tmpFile = open("tmp", "w")
		# read the last index in destination file and increment it to append new words
		tmpLine = g.readline()
		i = int(tmpLine[:-1] if tmpLine[-1] == "\n" else tmpLine)
		i += 1
		# copy temporarily the distination file in the tmp file 
		line = g.readline()
		while line != "":
			tmpFile.write(line)
			line = g.readline()
		g.close()
		tmpFile.close()
		# extract the words from the 'path' file and put them in a list
		g = open(destination, "w")
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
		# write the new last index
		g.write(str(i + j - 1) + "\n")
		# recopy the content of tmp file into the destination file
		tmpFile = open("tmp", "r")
		line = tmpFile.readline()
		while line != "":
			g.write(line)
			line = tmpFile.readline()
		# append the new words from the 'path' file
		for key in dico:
			g.write(str(i) + ";" + key[1] + "\n")
			i += 1
			for word in key[0]:
				if word[-1] == "=":
					word = word[:-1]
				g.write(str(i) + ";" + word + "\n")
				i += 1
		# close the files
		f.close()
		g.close()
		tmpFile.close()
		os.remove("tmp")
	except Exception as e:
		raise e
	

		