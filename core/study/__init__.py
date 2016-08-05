import os
import os.path
import pickle
import random as rnd


class level(object):
	"""docstring for level"""

	def __init__(self, path):
		super(level, self).__init__()
		# initialise variables
		self.path = path
		self.words = {}
		self.choices = {}
		self.mastered = []
		self.needsReview = []
		self.wordsleft = []
		self.counter = 0
		# check whether .words & .choices files exists & init the .dat file if not found
		if not os.path.isfile(path + '.words'):
			raise Exception(path + '.words' + ' not found')
		if not os.path.isfile(path + '.choices'):
			raise Exception(path + '.choices' + ' not found')
		if not os.path.isfile(path + '.dat'):
			f = open(path + '.dat', "wb")
			pickle.dump(self.mastered, f)
			pickle.dump(self.needsReview, f)
			pickle.dump(self.wordsleft, f)
			f.close()
		# fill the variables from the files
		f = open(path + '.words', 'rb')
		pickle.load(f) # last index, we r not gonna need it here
		self.words = pickle.load(f)
		f.close()
		f = open(path + '.choices', 'rb')
		self.choices = pickle.load(f)
		f.close()
		f = open(path + '.dat', 'rb')
		self.mastered = pickle.load(f)
		self.needsReview = pickle.load(f)
		self.wordsleft = pickle.load(f)
		f.close()
		# check whether the progress in the level is consistent ie every word is either mastered or needsReview or not prompted yet 
		if len(self.wordsleft) + len(self.mastered) + len(self.needsReview) < len(self.choices):
			self.wordsleft = list(self.choices.keys())
			self.mastered = []
			self.needsReview = []
		self.save()

	def save(self):
		# save progress
		f = open(self.path + '.dat', "wb")
		pickle.dump(self.mastered, f)
		pickle.dump(self.needsReview, f)
		pickle.dump(self.wordsleft, f)
		f.close()

	def addMastered(self, wordId):
		# add the word to the mastered set
		if wordId in self.wordsleft:
			self.wordsleft.remove(wordId)
		if wordId in self.needsReview:
			self.needsReview.remove(wordId)
		if wordId in self.mastered:
			return
		self.mastered += [wordId]

	def reset(self):
		# make things as it should be in first place
		self.wordsleft = list(self.choices.keys())
		self.mastered = []
		self.needsReview = []

	def addNeedsReview(self, wordId):
		# add the word to the needs review set
		if wordId in self.wordsleft:
			self.wordsleft.remove(wordId)
		if wordId in self.mastered:
			self.mastered.remove(wordId)
		if wordId in self.needsReview:
			return
		self.needsReview += [wordId]



	def getWord(self):
		'''
		get a word as an object:
		(
			wordId, 
			[
				word, 
				[choice1, choice2, choice3, choice4],
				correct choice
			]
		)
		'''
		while True: # if it didn't find a word with the specific index, increase it and try again
			self.counter += 1
			if self.counter % 10 == 0 and len(self.mastered) > 0: # each 10 times review a mastred word
				r = rnd.randrange(0, len(self.mastered))
				return (self.mastered[r],
					[self.words[self.mastered[r]],
					[self.words[i] for i in self.choices[list(self.mastered)[r]][0]],
					self.words[self.choices[list(self.mastered)[r]][1]]])
			if self.counter % 4 == 0 and len(self.needsReview) > 0: # each 4 times review a needsReview word
				r = rnd.randrange(0, len(self.needsReview))
				return (self.needsReview[r],
					[self.words[self.needsReview[r]],
					[self.words[i] for i in self.choices[list(self.needsReview)[r]][0]],
					self.words[self.choices[list(self.needsReview)[r]][1]]])
			# get a new word
			if len(self.wordsleft) > 0:
				r = rnd.randrange(0, len(self.wordsleft))
				return (self.wordsleft[r],
					[self.words[self.wordsleft[r]],
					[self.words[i] for i in self.choices[self.wordsleft[r]][0]],
					self.words[self.choices[self.wordsleft[r]][1]]])








		