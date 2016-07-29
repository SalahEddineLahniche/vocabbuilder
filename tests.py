import pickle
import os
import os.path
import core
import core.parser

# check wether we can parse the dico file returns 1 if success
def test1():
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

# check wether we can parse the dico file and append the results
def test2():
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

def dispose():
	if os.path.isfile('dicoN.words'):
		os.remove('dicoN.words')
	if os.path.isfile('dicoN.choices'):
		os.remove('dicoN.choices')



# de the tests
ans = test1()
if ans == 1:
	ans = test2()


if ans == 1:
	print("\ntests passed successfully")

# removes files
dispose()