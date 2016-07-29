import os
import os.path
import pickle

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

class config(object):
	"""docstring for config"""
	def __init__(self, path):
		super(config, self).__init__()

		self.path = path
		self.levels = []

		if not os.path.isfile(path):
			f = open(path, 'wb')
			pickle.dump(self.levels, f)
			f.close()

		f = open(path, 'rb')
		self.levels = pickle.load(f)

	def save(self):
		f = open(path, 'wb')
		pickle.dump(self.levels, f)
