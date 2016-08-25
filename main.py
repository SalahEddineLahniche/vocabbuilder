import core
import os
import os.path
import core.predef
import crypter
import textwrap
import dicoGenerator
currentLocation = "master"
sections = ["study", "game", "master"]
globalCmds = ["goto", "exit", "goback", "help", "cls"]
masterCmds = ['add-level', 'show-levels', 'dicoGenerator']
studyCmds = ['start', 'set-level', 'show-progress', 'show-levels']
gameCmds = []
exitCode = 0

wordsPath = "data/words.dat"
        

def exc(cmd):
	global currentLocation
	cmd = cmd.split()
	if len(cmd) < 1:
		print()
		return
	if(cmd[0] == "exit"):
		cmd_exit()
	elif(cmd[0] == "goback"):
		cmd_goback()
	elif(cmd[0] == "cls"):
		cmd_cls()
	elif(cmd[0] == "goto"):
		cmd_goto(cmd)
	elif(cmd[0] == "-h"):
		cmd_help(["all"])
	elif(cmd[0] == "help"):
		cmd_help(cmd)
	elif(curr() == "master"):
		if(cmd[0] == 'add-level'):
			cmd_add(cmd)
		elif(cmd[0] == 'show-levels'):
			cmd_show(cmd)
		elif(cmd[0] == 'dicoGenerator'):
			cmd_generate(cmd)
		else:
			err(cmd[0], 'nr')
			cmd_help()
	elif(curr() == "study"):
		if(cmd[0] == 'start'):
			cmd_start_study(cmd)
		elif(cmd[0] == 'set-level'):
			cmd_setLevel(cmd)
		elif(cmd[0] == 'show-progress'):
			cmd_show_progress(cmd)
		elif(cmd[0] == 'show-levels'):
			cmd_show(cmd)
		else:
			err(cmd[0], 'nr')
			cmd_help()

	else:
		err(cmd[0], 'nr')
		cmd_help()
		
def cmd_generate(cmd):
	dicoGenerator.init()
	if len(cmd) == 2:
		dicoGenerator.filename = cmd[1]
	if len(cmd) == 3:
		dicoGenerator.filename = cmd[1]
		dicoGenerator.append = True if 'True' in cmd[2] else False
	dicoGenerator.words = core.words(wordsPath)
	dicoGenerator.main()


def cmd_cls():
	os.system('cls')

def cmd_show_progress(cmd):
	global progress, conf
	for i in conf.levels:
		tmp = core.level('data/{}'.format(i[0] + '.dat'))
		print("your progress in level {}: {} left, {} mastered, Success rate: {}".format(i[1],
			str(len(tmp.wordsleft)), str(len(tmp.mastered)), tmp.successPercentageString()))
		del tmp


def cmd_setLevel(cmd):
	global conf
	echo('Setting current level to:\n')
	if len(cmd) == 2 and type(cmd[1] == type((0,))):
		print(cmd[1][1])
		conf.curr = cmd[1]
	else:
		cmd_show(None)
		i = input('Choose level: ')
		while not (i.isnumeric() or (i in range(len(conf.levels)))):
			err('incorrect choice')
			i = input('Choose level: ')
		conf.curr = conf.levels[int(i)]
		print(conf.curr[1])
	print("Set successfully")

def cmd_start_study(cmd):
	global progress, conf
	os.system("cls")
	print('Starting level {}'.format(str(conf.curr[1])))
	progress = core.level("data/" + str(conf.curr[0]) + '.dat')
	if check_completed():
			echo('this level is already completed, do you want to restudy it? (y|n):')
			res = input()
			if res == 'y':
				progress.reset()
			else:
				print('Please use set-level command to choose the level you want')
				return
	print("choose the right answer or type end to goback to study\n")
	ans = 'no meaning at all'
	dico = core.words(wordsPath)
	while ans != "end":
		os.system("cls")
		br = False
		w = progress.getWord()
		core.printWord(w, dico)
		while True:
			ans = input("you choose: ")
			print()
			if (not ans.isnumeric()) and ans!="":
				if not ans == 'end':
					err('choose the right answer or type end to goback to study')
					continue
				else:
					br = True
					break
			if (int(ans) >= len(w.choicesIds) + 1):
				err('choose a correct number from 0 to {}'.format(str(len(w.choicesIds))))
				continue
			break
		if br:
			br = False
			break
		if(ans == '' or ans == str(len(w.choicesIds)) or w.choicesIds[int(ans)] != w.correctChoiceId):
			progress.addNeedsReview(w.wordId)
			echo("not correct ! it means {} \n".format(dico.dico[w.correctChoiceId]))
		else:
			progress.addMastered(w.wordId)
			if check_completed():
				level_completed()
				break
			echo("correct, {} means {} \n".format(dico.dico[w.wordId], dico.dico[w.correctChoiceId]))
		print("your progress is now {} left, {} mastered, {} needs review".format(
			str(len(progress.wordsleft)), str(len(progress.mastered)), str(len(progress.needsReview))))
		print()
		ans = input("leave blank for next word or type 'end' to goback to study:")
	progress.save()

	
def cmd_add(cmd):
	global conf
	if len(cmd) < 2:
		err("incorrect usage of command 'add-level', try 'help add-level' for more inforamtion")
		return
	lev = core.parse(cmd[1], wordsPath)
	for el in lev:
		tmp = core.level('data/' + el[0] + '.dat')
		print('{} added successfully, file path: {}'.format(el[1], './data/' + el[0] + '.dat'))
		del tmp
	if conf.curr == '' and len(lev) > 0:
		conf.curr = lev[0]
	print("level {} is the current level".format(conf.curr[1]))
	conf.levels += lev

def cmd_show(cmd):
	global conf
	for i, lev in enumerate(conf.levels):
		print('{} - Level: {}, Path: {}'.format(str(i), lev[1], lev[0]))	

def cmd_goto(cmd):
	if(len(cmd) < 2):
		err("'blank'", "nr")
		return
	if(cmd[1] not in sections):
		err(cmd[1], "nr")
		return
	if(curr() != "master"):
		cmd_goback()
	addLevel(cmd[1])

def cmd_exit(cmd = []):
	global exitCode
	exitCode = 1

def cmd_goback():
	if(curr() != "master"):
		global currentLocation
		tmp = currentLocation.split(" $ ")
		tmp.pop()
		currentLocation = " $ ".join(tmp)
	else:
		err("where the hell u wanna go back !")

def cmd_help(cmd = []):
	if len(cmd) == 0:
		print("try '-h' to view all commands")
		return
	elif len(cmd) == 1:
		if(cmd[0] == "all"):
			if curr() == "master":
				for cmd in globalCmds:
					print(cmd)
				for cmd in masterCmds:
					print(cmd)
				return
			if curr() == "study":
				for cmd in globalCmds:
					print(cmd)
				for cmd in studyCmds:
					print(cmd)
				return
			if curr() == "game":
				for cmd in globalCmds:
					print(cmd)
				for cmd in gameCmds:
					print(cmd)
				return
		if cmd[0] == "help":
			print("specify a command to get help or type '-h' to show all available commands")
	else:
		if(cmd[1] == "goto"):
			print("go to a specefic section: study or game")
		elif(cmd[1] == "goback"):
			print("go back to master")
		elif(cmd[1] == "exit"):
			print("exit the app")
		elif(cmd[1] == "cls"):
			print("clear the screen")
		elif(cmd[1] == "help"):
			print("get the help for the specific command")
		elif(cmd[1] == "add-level" and curr() == "master"):
			print("add a specefic level\n\nuse: add-level [path]\npath: a valid dictionary file")
		elif(cmd[1] == "show-levels"  and curr() == "master"):
			print("show existing levels")
		elif(cmd[1] == "show-progress"  and curr() == "study"):
			print("show current progress for existing levels")
		elif(cmd[1] == "set-level"  and curr() == "study"):
			print("set a level to study\n\nuse: 'set-level' then '[a number indicating the level u choose]'")
		elif(cmd[1] == 'dicoGenerator' and curr() == 'master'):
			print("Creat a dictionary from scratch and save it to a file\n")
			print("use: dicoGenerator [filename] [True|False]{append or overwrite}")
		else:
			err(cmd[1], "nr")
			print("try '-h' to view all commands")


def check_completed():
	return len(progress.mastered) == len(progress.levelChoices.choices)

def level_completed():
	print('----------------- !! great work !! -----------------')
	print('level {} is completed'.format(str(conf.curr[1])))
	prompt = False
	for lev in (conf.levels):
		if lev != conf.curr and not prompt:
			continue
		if not prompt:
			prompt = True
			continue
		echo('Do you wanna pass to level {} (y|n):'.format(lev[1]))
		while True:
			ans = input()
			if ans == 'y':
				cmd_setLevel(['set-level', lev])
				return
			elif ans == 'n':
				break
			else:
				err('Expecting y or n')
				echo('You choose: ')
		break
	print('Please use set-level command to choose the level you want')



def initCmd():
	global currentLocation, conf
	if len(conf.levels) == 0 and curr() == 'study':
			print('[*] No levels found...!')
			print('Adding Built in levels')
			cmd_add(['add', '~$tmp_dico'])
	print("\n", currentLocation, ": ", end='', sep="")
	if curr() == 'study':
		echo('<Current level: {}> '.format(str(conf.curr[1])))
	exc(input())

def echo(string):
	print(string, end='')

def addLevel(level):
	global currentLocation
	if curr() == level:
		return
	currentLocation += " $ " + level

def curr():
	global currentLocation
	return currentLocation.split(" $ ")[-1]


def firstMessage():
	msg = '''\
	Vocabbuilder - command-line
	Program that aims building a vocabulary for english learner by a set of commun & must-know words
	To start, if u have already a dictionary file, in master execute 'add-level [yourfile]' else
	there is a built-in dictionary ready for u to use.
	whenever started, type 'goto study', 'set-level', to set a level as current level for studying.
	Also u can type 'show-progress' in study section to view ur progress in all existing levels.
	'''
	msg = textwrap.dedent(msg)
	print(msg) 

def err(strErr, errType=""):
	echo('-!- : ')
	if(errType == "nr"):
		echo(strErr + " is not recognized\n\n")
	elif(errType == ""):
		echo(strErr + "\n\n")
if not os.path.isdir('data'):
	os.mkdir('data')
conf = core.config('data/config.dat')
progress = None

if len(conf.levels) == 0:
	f = open('~$tmp_dico', 'w')
	f.write(crypter.decrypt(core.predef.BUILT_IN_DICO))
	f.close()

os.system("cls")
firstMessage()
while(exitCode == 0):
	initCmd()
conf.save()

echo("\nexited with code " + str(exitCode))
