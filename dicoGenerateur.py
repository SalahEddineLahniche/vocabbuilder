def getStr(cmd):
	string = ''
	if cmd[0] == 'add':
		string += cmd[1].replace('-', ' ')
		string += ';'
		string += cmd[2].replace('-', ' ')
		string += '=.'
		for i in cmd[3:]:
			string += i.replace('-', ' ')
			string += '.'
	string = string[:-1]
	string += '\n'
	return string

ans = input('<=> ')
f = open('dicoN', 'a')
while ans != 'end':
	cmd = ans.split()
	f.write(getStr(cmd))
	ans = input('<=> ')

f.close()


