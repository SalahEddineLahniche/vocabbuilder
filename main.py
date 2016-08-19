import core
import os
import os.path
import core.predef
import crypter
import textwrap

# a variable that holds the current location whether it's master or master $ study ...etc
currentLocation = "master"
# available section for goto commands
sections = ["study", "game", "master"]
# available commands, each in it's section. for global commands they work in all sections
globalCmds = ["goto", "exit", "goback", "help", "cls"]
masterCmds = ['add-level', 'show-levels']
studyCmds = ['start', 'set-level', 'show-progress', 'show-levels']
gameCmds = []
# exit code, if not 0 the program exits the main loop
exitCode = 0

wordsPath = "data/words.dat"
        

def exc(cmd):
	'''
	execute the command.

	cmd: a command like 'goto study' or 'add-level ../dicotionary.dat'

	no return
	'''
	global currentLocation
	# split the commands for main & sub-commands & eventually flags
	cmd = cmd.split()
	if len(cmd) < 1:
		print()
		return
	# select the case and execute the appropriate command.
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

		
#Commands
def cmd_cls():
	'''
	clear the screen
	'''
	os.system('cls')

def cmd_show_progress(cmd):
	'''
	show the current progress for all levels

	cmd: the command as a list ['show-progress']

	no returns
	'''
	global progress, conf
	# itirate over all levels that exists in in the config file
	for i in conf.levels:
		# initiate a level class, that loads all variable needed for determening progress
		tmp = core.level('data/{}'.format(i[0] + '.dat'))
		# print the progress
		print("your progress in level {}: {} left, {} mastered, {} needs review".format(i[1],
			str(len(tmp.wordsleft)), str(len(tmp.mastered)), str(len(tmp.needsReview))))
		# unalocate the memory for the tmp variable
		del tmp


def cmd_setLevel(cmd):
	'''
	set the current level, to a level from existing levels

	cmd: the command as list ['set-level', 'level's number']

	no returns
	'''
	global conf
	# we need a level number, if not given it's an incorrect usage
	cmd_show(None)
	i = input('Choose level: ')
	while not (i.isnumeric() or (i in range(len(conf.levels)))):
		err('incorrect choice')
		i = input('Choose level: ')
	print('Setting current level to level {}'.format(conf.levels[int(i)][1]))
	# the param should be numeric
	conf.curr = conf.levels[int(i)]

def cmd_start_study(cmd):
	'''
	start the current level or start a specific level

	cmd: the command as a list ['start'] or ['start', 'level's number']

	no returns
	'''
	global progress, conf
	# starting a specific level means setting it first & start it normally
	# if len(cmd) > 1:
	# 	cmd_setLevel(['set-level', cmd[1]])
	print('Starting level {}'.format(str(conf.curr[1])))
	# load the level class of the level
	progress = core.level("data/" + str(conf.curr[0]) + '.dat')
	# check if the level is already mastered & prompt the user for restuding it 
	if check_completed():
			echo('this level is already completed, do you want to restudy it? (y|n):')
			res = input()
			if res == 'y':
				progress.reset()
			else:
				print('Please use set-level command to choose the level you want')
				return
	print("choose the right answer or type end to goback to study\n")
	# this ans have no meaning at all just to start the while
	ans = 'no meaning at all'
	dico = core.words(wordsPath)
	while ans != "end":
		# get a word randomley from the levels database
		w = progress.getWord()
		# print the choices nicely 
		core.printWord(w, dico)
		ans = input("you choose: ")
		print()
		# 'blank' means i don't know, a number is expected or end command. if not pass to the next question
		if (not ans.isnumeric()) and ans!="":
			if not ans == 'end':
				echo('choose the right answer or type end to goback to study -- PASSING TO NEXT QUESTION\n')
			continue
		# check if the answer is correct
		if(ans == '' or ans == str(len(w.choicesIds)) or w.choicesIds[int(ans)] != w.correctChoiceId):
			progress.addNeedsReview(w.wordId)
			echo("not correct ! it means {} \n".format(dico.dico[w.correctChoiceId]))
		else:
			progress.addMastered(w.wordId)
			if check_completed():
				level_completed()
				break
			echo("correct, {} means {} \n".format(dico.dico[w.wordId], dico.dico[w.correctChoiceId]))
		# print progress
		print("your progress is now {} left, {} mastered, {} needs review".format(
			str(len(progress.wordsleft)), str(len(progress.mastered)), str(len(progress.needsReview))))
		print()
		# prompt the user if he want to suspend the study
		ans = input("leave blank for next word or type 'end' to goback to study:")
	# save the progress whenever exited
	progress.save()
	

	
def cmd_add(cmd):
	'''
	add a level from an existing file

	cmd: command as list ['add-level', 'file path']

	no returns
	'''
	global conf
	# we need a path, if not given it's an incorrect usage
	if len(cmd) < 2:
		err("incorrect usage of command 'add-level', try 'help add-level' for more inforamtion")
		return
	# add the level to the data folder
	lev = core.parse(cmd[1], wordsPath)
	for el in lev:
		tmp = core.level('data/' + el[0] + '.dat')
		print('{} added successfully, file path: {}'.format(el[1], './data/' + el[0] + '.dat'))
		del tmp
	# if no level is set as the current level, set this level as the current level
	if conf.curr == '' and len(lev) > 0:
		conf.curr = lev[0]
	print("level {} has been set as current level".format(conf.curr[1]))
	# add this level to the config file
	conf.levels += lev
	# initiate the level

def cmd_show(cmd):
	'''
	show current levels

	cmd: the command as list ['show-levels'] expected

	no returns
	'''
	global conf
	for i, lev in enumerate(conf.levels):
		print('{} - Level: {}, Path: {}'.format(str(i), lev[1], lev[0]))	

def cmd_goto(cmd):
	'''
	goto a specific section

	cmd: the command as list ['goto', '!a section!']

	no returns
	'''
	# we need a section, if not given it's an incorrect usage
	if(len(cmd) < 2):
		err("'blank'", "nr")
		return
	if(cmd[1] not in sections):
		err(cmd[1], "nr")
		return
	# if u'r not in the master section, we need to go back first
	if(curr() != "master"):
		cmd_goback()
	# update the current location
	addLevel(cmd[1])

def cmd_exit(cmd = []):
	'''
	exit the program, !with a specific exit code if cmd is given!

	cmd: the command as list 'TODO: what type of cmd should be exit with another exitCode

	no returns
	'''
	global exitCode
	exitCode = 1

def cmd_goback():
	'''
	go back to master section

	no returns
	'''
	if(curr() != "master"):
		global currentLocation
		tmp = currentLocation.split(" $ ")
		tmp.pop()
		currentLocation = " $ ".join(tmp)
	else:
		err("where the hell u wanna go back !")

def cmd_help(cmd = []):
	'''
	get help for a specific commad or show all commands

	cmd: ['all'] to show all command in the current section, ['help', '!a command!'] to view help for a specific command

	no returns
	'''
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
			print("set a level to study\n\nuse: set-level [number]\nthe parameter is the index of level."
				" goback to master then type 'show-levels' to view existing levels")
		else:
			err(cmd[1], "nr")
			print("try '-h' to view all commands")


def check_completed():
	'''
	check if level is completed
	'''
	return len(progress.mastered) == len(progress.levelChoices.choices)

def level_completed():
	'''
	the command to execute if level is completed

	no returns
	'''
	print('----------------- !! great work !! -----------------')
	print('level {} is completed'.format(str(conf.curr[1])))
	# check if there is a level ahead
	if max(conf.levels) > conf.curr:
		for i, lev in enumerate(conf.levels):
			# continue till u find a the current level, in order
			if lev != conf.curr:
				continue
			# prompt the user if he wants to pass to next level, otherwise he needs to choose a level himself
			echo('Do you wanna pass to level {} (y|n):'.format(lev[1]))
			while True:
				ans = input()
				if ans == 'y':
					cmd_setLevel(['set-level', str(i)])
					return
				elif ans == 'n':
					break
				else:
					err('Expecting y or n')
					echo('You choose: ')
			break
	print('Please use set-level command to choose the level you want')



def initCmd():
	'''
	write the current location and waits for user command then execute it

	no retruns
	'''
	global currentLocation, conf
	if len(conf.levels) == 0 and curr() == 'study':
			print('No levels found...!')
			print('Adding Built in levels')
			cmd_add(['add', '~$tmp_dico'])
	print("\n", currentLocation, ": ", end='', sep="")
	if curr() == 'study':
		echo('<Current level: {}> '.format(str(conf.curr[1])))
	exc(input())

def echo(string):
	'''
	print without end line

	no returns
	'''
	print(string, end='')

def addLevel(level):
	'''
	update current location

	no returns
	'''
	global currentLocation
	if curr() == level:
		return
	currentLocation += " $ " + level

def curr():
	'''
	get the current location

	returns: current location as in sections variable
	'''
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
	'''
	print a message as a error

	strErr: message to print or user input
	errType: if equals 'nr' the it prints the the user input specified above is not recognized

	no returns
	'''
	echo('-!- : ')
	if(errType == "nr"): #not recognized error
		echo(strErr + " is not recognized\n\n")
	elif(errType == ""):
		echo(strErr + "\n\n")


# check if data folder exists, if not create it
if not os.path.isdir('data'):
	os.mkdir('data')
# load the config file
conf = core.config('data/config.dat')
# initialize the progress variable <core.study.level class>
progress = None

if len(conf.levels) == 0:
	f = open('~$tmp_dico', 'w')
	f.write(crypter.decrypt(core.predef.BUILT_IN_DICO))
	f.close()

firstMessage()
# main loop
while(exitCode == 0):
	initCmd()

# save the config file if everything goes normally
conf.save()

echo("\nexited with code " + str(exitCode))
