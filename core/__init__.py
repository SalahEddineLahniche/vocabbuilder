import os
import os.path
import pickle
import re
import random as rnd


regexp = re.compile('([^;]+)(?=;)|([^;.]+)((?=.)|(?<=.))')

# print dico function
def printDico(dico):
	print("printing dico...\n-------")
	for key in dico:
		print(key, dico[key])
	print("-------")


def rndStr(length):
	tmp = [chr(i) for i in range(ord('a'), ord('f') + 1)] + [str(i) for i in range(10)]
	l = len(tmp)
	s = ''
	for j in range(length):
		r = rnd.randint(0, l - 1)
		s += tmp[r]
	return s

def padAndCenter(string, length):
	if len(string) > length:
		return string
	halfLength = length - len(string)
	halfLength = halfLength / 2
	halfLength = int(halfLength)
	string = " " * halfLength + string + " " * halfLength
	return (len(string), string)

def padr(string, length):
	if len(string) > length:
		return string
	return string + " " * (length - len(string))

def printWord(word, dico):
	length = 32
	length, fline = padAndCenter(dico.dico[word.wordId] + " means", length)
	sep = "-" * (length + 2)
	fline = "|" + fline + "|"
	print(sep)
	print(fline)
	j = 0
	for i, choice in enumerate(word.choicesIds):
		print(sep)
		print("|" + padr(" {} - {}".format(i, dico.dico[choice]), length) + "|")
		j = i
	print(sep)
	print("|" + padr(" {} - {}".format(j + 1, "I don't know"), length) + "|")
	print(sep)

def randomizeList(lst):
	length = len(lst)
	for i in range(length):
		a = rnd.randint(0, length - 1)
		b = rnd.randint(0, length - 1)
		lst[a], lst[b] = lst[b], lst[a]
	return lst

def parseLine(line, dico):
	matches = list(regexp.finditer(line))
	c = choice()
	c.wordId = dico.getId(matches[0].group(0))
	l = list(matches[1:])
	l = randomizeList(l)
	for m in l:
		if m.group(0)[-1] == '=':
			c.correctChoiceId = dico.getId(m.group(0)[:-1])
			c.choicesIds += [c.correctChoiceId]
			continue
		c.choicesIds += [dico.getId(m.group(0))]
	return c

def parse(path, wordsDicoPath):
	dico = words(wordsDicoPath)
	if not os.path.isfile(path):
			raise Exception('{} -- path doesn\'t exist'.format(path))
	f = open(path, 'r')
	levelName = 'not specified'
	levelFileName = rndStr(10)
	counter = 0
	levels = [(levelFileName, levelName)]
	l = f.readline()
	tmpChoices = levelChoices('data/' + levelFileName + '.dat')
	while l:
		if l[-1] == '\n':
			l = l[:-1]
		if l[0] == '#':
			tmpChoices.save()
			if counter == 0:
				levels.pop()
				os.remove('data/' + levelFileName + '.dat')
			levelName = l[1:]
			levelFileName = rndStr(10)
			tmpChoices = levelChoices('data/' + levelFileName + '.dat')
			counter = 0
			levels += [(levelFileName, levelName)]
		else:
			c = parseLine(l, dico)
			tmpChoices.choices[c.wordId] = c
			counter += 1
		l = f.readline()
	tmpChoices.save()
	dico.save()
	return levels

class config():
	"""docstring for config"""
	def __init__(self, path):
		self.path = path
		self.levels = []
		self.curr = ''

		if not os.path.isfile(self.path):
			f = open(self.path, 'wb')
			pickle.dump(self.levels, f)
			pickle.dump(self.curr, f)
			f.close()

		f = open(self.path, 'rb')
		self.levels = pickle.load(f)
		self.curr = pickle.load(f)
		f.close()

	def save(self):
		f = open(self.path, 'wb')
		pickle.dump(self.levels, f)
		pickle.dump(self.curr, f)
		f.close()

class words():
	"""docstring for words"""
	def __init__(self, path):
		self.path = path
		if not os.path.isfile(path):
			g = open(path, "wb")
			pickle.dump({}, g)
			g.close()
		f = open(path, 'rb')
		self.dico = pickle.load(f)

	def getId(self, word):
		for i in self.dico:
			if self.dico[i] == word:
				return i
		return self.addWord(word)

	def addWord(self, word):
		if word in self.dico.values():
			return getId(word)
		else:
			i = max(self.dico.keys()) + 1 if len(self.dico) > 0 else 0
			self.dico[i] = word
			return i

	def removeWord(self, word):
		if word in self.dico.values():
			del self[getId(word)]

	def save(self):
		g = open(self.path, "wb")
		pickle.dump(self.dico, g)
		g.close()

class choice():
	"""docstring for choice"""
	def __init__(self):
		self.wordId = -1
		self.correctChoiceId = -1
		self.choicesIds = []

class levelChoices():
	"""docstring for choices"""
	def __init__(self, path):
		self.path = path
		if not os.path.isfile(path):
			g = open(path, "wb")
			pickle.dump({}, g)
			g.close()
		f = open(path, 'rb')
		self.choices = pickle.load(f)

	def save(self):
		g = open(self.path, "wb")
		pickle.dump(self.choices, g)
		g.close()

class level(object):
	"""docstring for level"""

	def __init__(self, path):
		super(level, self).__init__()
		# initialise variables
		self.path = path
		self.levelChoices = None
		self.mastered = []
		self.needsReview = []
		self.wordsleft = []
		self.history = (0, 0)
		self.counter = 0
		if not os.path.isfile(path):
			raise Exception(path + ' not found')
		if not os.path.isfile(path + '-progress' + '.dat'):
			f = open(path + '-progress' + '.dat', "wb")
			pickle.dump(self.mastered, f)
			pickle.dump(self.needsReview, f)
			pickle.dump(self.wordsleft, f)
			pickle.dump(self.history, f)
			f.close()

		self.levelChoices = levelChoices(path)

		f = open(path + '-progress' + '.dat', 'rb')
		self.mastered = pickle.load(f)
		self.needsReview = pickle.load(f)
		self.wordsleft = pickle.load(f)
		self.history = pickle.load(f)
		f.close()
		# check whether the progress in the level is consistent ie every word is either mastered or needsReview or not prompted yet 
		if len(self.wordsleft) + len(self.mastered) + len(self.needsReview) < len(self.levelChoices.choices):
			self.wordsleft = list(c for c in self.levelChoices.choices)
			self.mastered = []
			self.needsReview = []
		self.save()

	def reset(self):
		self.wordsleft = list(c for c in self.levelChoices.choices)
		self.mastered = []
		self.needsReview = []
		self.save()

	def save(self):
		# save progress
		f = open(self.path + '-progress' + '.dat', "wb")
		pickle.dump(self.mastered, f)
		pickle.dump(self.needsReview, f)
		pickle.dump(self.wordsleft, f)
		pickle.dump(self.history, f)
		f.close()

	def successPercentageString(self):
		if self.history[1] + self.history[0] == 0:
			return '- %'
		return '{} %'.format(round((self.history[0] / (self.history[1] + self.history[0])) * 100, 2))

	def addMastered(self, wordId):
		# add the word to the mastered set
		if wordId in self.wordsleft:
			self.wordsleft.remove(wordId)
		if wordId in self.needsReview:
			self.needsReview.remove(wordId)
		if wordId in self.mastered:
			return
		self.history = (self.history[0] + 1, self.history[1])
		self.mastered += [wordId]

	def addNeedsReview(self, wordId):
		# add the word to the needs review set
		if wordId in self.wordsleft:
			self.wordsleft.remove(wordId)
		if wordId in self.mastered:
			self.mastered.remove(wordId)
		if wordId in self.needsReview:
			return
		self.history = (self.history[0], self.history[1] + 1)
		self.needsReview += [wordId]



	def getWord(self):
		while True: # if it didn't find a word with the specific index, increase it and try again
			self.counter += 1
			if self.counter % 10 == 0 and len(self.mastered) > 0: # each 10 times review a mastred word
				r = rnd.randrange(0, len(self.mastered))
				return self.levelChoices.choices[self.mastered[r]]
			if self.counter % 4 == 0 and len(self.needsReview) > 0: # each 4 times review a needsReview word
				r = rnd.randrange(0, len(self.needsReview))
				return self.levelChoices.choices[self.needsReview[r]]
			# get a new word
			if len(self.wordsleft) > 0:
				r = rnd.randrange(0, len(self.wordsleft))
				return self.levelChoices.choices[self.wordsleft[r]]


