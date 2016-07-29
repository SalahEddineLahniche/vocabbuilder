import pickle
import os
import os.path
import core
import core.parser
import core.study

# check wether we can parse the dico file returns 1 if success
def test1():
	try:
		# remove if dico and choices files already exists
		if os.path.isfile('dicoN.words'):
			os.remove('dicoN.words')
		if os.path.isfile('dicoN.choices'):
			os.remove('dicoN.choices')

		# parse the file and print the results of unpickled dicoN
		core.parser.parse('dico', 'dicoN')
		f = open('dicoN.words', 'rb')
		i = pickle.load(f)
		print(i)
		dico = pickle.load(f)
		core.printDico(dico)

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1

		# print the results of unpickled dicoN.choices
		f = open('dicoN.choices', 'rb')
		dico = pickle.load(f)
		core.printDico(dico)

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1

		# succcess
		return 1
	except Exception as e:
		# failure
		return -1

# check wether we can parse the dico file and append the results
def test2():
	try:
		# remove if dico and choices files already exists
		if os.path.isfile('dicoN.words'):
			os.remove('dicoN.words')
		if os.path.isfile('dicoN.choices'):
			os.remove('dicoN.choices')

		# parse the file and print the results of unpickled dicoN
		core.parser.parse('dico', 'dicoN')
		core.parser.parse('dico', 'dicoN')
		f = open('dicoN.words', 'rb')
		i = pickle.load(f)
		print(i)
		dico = pickle.load(f)
		core.printDico(dico)

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1

		# print the results of unpickled dicoN.choices
		f = open('dicoN.choices', 'rb')
		dico = pickle.load(f)
		core.printDico(dico)

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1

		# succcess
		return 1
	except Exception as e:
		# failure
		return -1

def test3():
	try:
		# remove if dico and choices files already exists
		if os.path.isfile('dicoN.words'):
			os.remove('dicoN.words')
		if os.path.isfile('dicoN.choices'):
			os.remove('dicoN.choices')
		# create the .words & .choices
		core.parser.parse('dico', 'dicoN')
		l = core.study.level('dicoN')
		# get 10 next word & print them
		w = [l.getWord() for i in range(10)]
		for wrd in w:
			core.printWord(wrd, True)
			print()
		# test adding words to different sections
		print("before:")
		print(l.wordsleft)
		print(l.mastered)
		print(l.needsReview)
		l.addMastered(w[0][0])
		l.addMastered(w[1][0])
		l.addNeedsReview(w[2][0])
		l.addNeedsReview(w[3][0])
		print("after:")
		print(l.wordsleft)
		print(l.mastered)
		print(l.needsReview)

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1
		# check whether the choice of words is consistent, each 4 words a needs review word
		print('level.counter:', str(l.counter))
		w = [l.getWord() for i in range(10)]
		for wrd in w:
			core.printWord(wrd, True)
			print()

		ans = input("is everything works fine:")
		if not ans == "":
			# faillure
			return -1

		# success
		return 1
	except Exception as e:
		# faillure
		raise e
		return -1




def dispose():
	if os.path.isfile('dicoN.words'):
		os.remove('dicoN.words')
	if os.path.isfile('dicoN.choices'):
		os.remove('dicoN.choices')
	if os.path.isfile('dicoN.dat'):
		os.remove('dicoN.dat')


cmd = input('choose the test:\n')
if cmd != '':
	exec('ans = test' + cmd + '()')
else:
	# do all the tests
	ans = test1()
	if ans == 1:
		ans = test2()
	if ans == 1:
		ans = test3()


if ans == 1:
	print("\ntests passed successfully")

# removes files
dispose()