import os
import os.path

filename = 'dicoN'
append = False	

def getStr(cmd):
	string = ''
	if cmd[0] == 'add':
		string += cmd[1].replace('_', ' ')
		string += ';'
		string += cmd[2].replace('_', ' ')
		string += '=.'
		for i in cmd[3:]:
			string += i.replace('_', ' ')
			string += '.'
		string = string[:-1]
	if cmd[0] == 'level':
		string += '#{}'.format(cmd[1].replace('_', ' '))
	string += '\n'
	return string

def init():
	global filename, append
	filename = 'dicoN'
	append = False

def main():
	global filename, append
	print('Dico Generator, file name = {}, append = {}\n\n'.format(filename, append))
	print('Usage: add [word] [synonym] [choice1] [choice2] ...')
	print('Usage: level [newLevelName]')
	print('replace a space in words by \'_\'\n')

	if os.path.isfile(filename) and append == False:
		print('{} already exists do you want o overwrite (y|n):'.format(filename), end="")
		while True:
			ans = input()
			if ans == 'n':
				append = False
			elif ans == 'y':
				append = True
			else:
				print("overwrite ? (y|n)", end="")
				continue
			break
	if not append:
		print('Please specify a level\'s name !')
	ans = 'level ' + input('<=> level ')
	f = open(filename, 'a' if append else 'w')
	f.write(getStr(ans.split()))
	ans = input('<=> ')
	while ans != 'end':
		cmd = ans.split()
		f.write(getStr(cmd))
		ans = input('<=> ')

	f.close()


