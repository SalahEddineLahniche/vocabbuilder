
# print dico function
def printDico(dico):
	print("printing dico...\n-------")
	for key in dico:
		print(key, dico[key])
	print("-------")

def printWord(word, debug=False):
	if debug:
		print(word[0])
	print("{} means:".format(word[1][0]))
	j = 0
	for i, choice in enumerate(word[1][1]):
		print("{} - {}".format(i, choice))
		j = i
	print("{} - {}".format(j + 1, "I don't know"))