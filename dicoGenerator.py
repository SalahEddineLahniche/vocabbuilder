import os
import os.path
import random as rnd
import core
import textwrap

filename = 'dicoN'
append = False
words = None

def evaluate(cmd):
	string = ''
	if cmd[0] == 'add':
		string += cmd[1].replace('_', ' ')
		string += ';'
		string += cmd[2].replace('_', ' ')
		string += '=.'
		j = 1
		for i in cmd[3:]:
			if i == "$":
				i = getWord(j)
			if i == "#":
				lst = list(words.dico.keys())
				r = rnd.randint(0, len(lst) - 1)
				while True:
					ans = input("[choice %d] We have chosen '%s' as a random FALSE meaning for '%s'. procced ? (y|n)" % 
						        (j, words.dico[lst[r]], cmd[1].replace('_', ' ')))
					if ans == "y":
						i = words.dico[lst[r]]
						break
					elif ans == "n":
						r = rnd.randint(0, len(lst) - 1)
						continue
					else:
						print("Incorrect choice answer by 'y' or 'n'")
			string += i.replace('_', ' ')
			string += '.'
			j += 1
		string = string[:-1]
	if cmd[0] == 'level':
		string += '#{}'.format(cmd[1].replace('_', ' '))
	if cmd[0] == 'view':
		g = open(filename, "r")
		line = g.readline()
		level = ""
		print("[*] Begining\n")
		while line:
			line = line.rstrip()
			if line[0] == "#":
				level = line[1:]
				w = None
			else:
				w = core.parseLineString(line)
			if level and w:
				print(textwrap.dedent("""\
					 [level %s] - '%s' means '%s'
					 -> Choices %s\
					 """ % (level, w.wordId, w.correctChoiceId, ", ".join("'" + w.choicesIds + "'"))))
			line = g.readline()
		g.close()
		print("\n[*] End")
		return None

	string += '\n'
	return string

def printDico(dico, start, length):
	r = max(dico.keys())
	lst = []
	os.system("cls")
	while length > 0 and start <= r:
		if dico.get(start):
			print("[*] %d - %s" % (start, dico[start]))
			lst += [start]
		start += 1
		length -= 1
	return lst

def getWord(j):
	i = min(words.dico.keys())
	while True:
		lst = printDico(words.dico, i, 15) + [""]
		if len(lst) == 1:
			print("[!] end of dictionary...", end="")
			ans = input("Do you want to start all over again ? (y|n):")
			while True:
				if ans == "y":
					i = min(words.dico.keys())
					break
				elif ans == "n":
					return input("Write then the word to be the choice:")
				else:
					print("Incorrect choice, (y|n) ?", end="")
					ans = input()
					continue
			continue
		print("[choice %d] - you choose (leave blank for next page):" % j, end="")
		ans = input()
		ans = int(ans) if ans.isnumeric() else ans
		while(True):
			if ans not in lst:
				print("Incorrect choice, a number from above or blank to next page:", end="")
				ans = input()
				continue
			if ans == "":
				i = max(lst[:-1]) + 1
				break
			return words.dico[ans]
		continue

def init():
	global filename, append
	filename = 'dicoN'
	append = False

def main():
	global filename, append
	print('Dico Generator, file name = {}, append = {}\n\n'.format(filename, append))
	print('Usage: add [word] [synonym] [choice1] [choice2] ...')
	print('Usage: level [newLevelName]')
	print('Usage: \'view\' to view current status')
	print('replace [choice] by $ if u want to go through the dictionary for a convenient choice')
	print('replace [choice] by # if u want to choose randomly a word from the dico')
	print('replace a space in words by \'_\'\n')

	if os.path.isfile(filename) and append == False:
		print('{} already exists do you want to overwrite (y|n):'.format(filename), end="")
		while True:
			ans = input()
			if ans == 'n':
				append = True
			elif ans == 'y':
				append = False
			else:
				print("overwrite ? (y|n)", end="")
				continue
			break
	ans = ""
	f = open(filename, 'a' if append else 'w')
	if not append:
		print('Please specify a level\'s name !')
		ans = 'level ' + input('<=> level ')
		f.write(evaluate(ans.split()))
	ans = input('<=> ')
	while ans != 'end':
		cmd = ans.split()
		e = evaluate(cmd)
		if e:
			f.write(e)
			f.flush()
		ans = input('\n<=> ')

	f.close()


