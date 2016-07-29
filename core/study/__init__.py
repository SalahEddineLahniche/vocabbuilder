import os
import os.path
import pickle
import random as rnd


class level(object):
	"""docstring for level"""

	def __init__(self, path):
		super(level, self).__init__()

		self.path = path
		self.words = {}
		self.choices = {}
		self.mastered = []
		self.needsReview = []
		self.wordsleft = []
		self.counter = 0

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

		if len(self.wordsleft) + len(self.mastered) + len(self.needsReview) < len(self.words):
			self.wordsleft = list(self.choices.keys())
			self.mastered = []
			self.needsReview = []

	def Save(self):
		f = open(path + '.dat', "wb")
		pickle.dump(self.mastered, f)
		pickle.dump(self.needsReview, f)
		pickle.dump(self.wordsleft, f)
		f.close()

	def addMastered(self, wordId):
		if wordId in self.wordsleft:
			self.wordsleft.remove(wordId)
		if wordId in self.needsReview:
			self.needsReview.remove(wordId)
		self.mastered += [wordId]



	def getWord(self):
		if self.counter % 10 == 0 and len(self.mastered) > 0:
			r = rnd.randrange(0, len(self.mastered))
			return (self.wordsleft[r],
				[self.words[self.wordsleft[r]],
				[self.words[i] for i in self.choices[list(self.mastered.keys())[r]][0]],
				self.words[self.choices[list(self.mastered.keys())[r]][1]]])
		if self.counter % 4 == 0 and len(self.needsReview) > 0:
			r = rnd.randrange(0, len(self.needsReview))
			return (self.wordsleft[r],
				[self.words[self.wordsleft[r]],
				[self.words[i] for i in self.choices[list(self.needsReview.keys())[r]][0]],
				self.words[self.choices[list(self.needsReview.keys())[r]][1]]])
		r = rnd.randrange(0, len(self.wordsleft))
		return (self.wordsleft[r],
			[self.words[self.wordsleft[r]],
			[self.words[i] for i in self.choices[self.wordsleft[r]][0]],
			self.words[self.choices[self.wordsleft[r]][1]]])








		