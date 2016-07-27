import os.path
import os
import pickle

#takes a file with the format of
#word;choice1.correct choice2=.choice3
##section
#word;choice1.correct choice2=.choice3
#and transforme it to a file
# last index:int
# {id: word}
def parse(path, destination):
	try:
		# check whether the files exists & init the destination if not already initialised
		if not os.path.isfile(path):
			return -1
		if not os.path.isfile(destination):
			g = open(destination, "wb")
			pickle.dump(0, g)
			pickle.dump({}, g)
			g.close()
		# open the files
		f = open(path)
		g = open(destination, "rb")
		# unpickle the destination file and increment the last index
		i = pickle.load(g)
		i += 1
		lst = pickle.load(g)
		g.close()
		g = open(destination, 'wb')
		# extract the words from the 'path' file and put them in a list
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
		# update the choices file
		addChoices(destination, dico, i)
		# append the new words from the 'path' file
		for key in dico:
			lst[i] = key[1]
			i += 1
			for word in key[0]:
				if word[-1] == "=":
					word = word[:-1]
				lst[i] = word
				i += 1
		# write the new last index and the dico
		pickle.dump(i - 1, g)
		pickle.dump(lst, g)
		# close the files
		g.close()
		f.close()
	except Exception as e:
		raise e
	
# creates the .choices file
def addChoices(path, lst, i):
	try:
		# open the file or create it if it doesn't exists
		path = path + ".choices"
		if not os.path.isfile(path):
				g = open(path, "wb")
				pickle.dump({}, g)
				g.close()
		# open for append
		g = open(path, "rb")
		# unpickle to update
		dico = pickle.load(g)
		g.close()
		# init the starting index
		j = i
		# append the choices
		for el in lst:
			for x in range(len(el[0])):
				if el[0][x][-1] == "=":
					dico[j] = [list(range(j + 1, j + 1 + len(el[0])))] + [j + 1 + x]
					break
			j += 1 + len(el[0])
		# reopen & pickle changes
		g = open(path, 'wb')
		pickle.dump(dico, g)
		# close the file
		g.close()
	except Exception as e:
		raise e


