import core
import core.parser
import core.study
import core.game
import os
import os.path

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
        

def exc(cmd):
	'''
	execute the command.

	cmd: a command like 'goto study' or 'add-level ../dicotionary.dat'

	no return
	'''
	global currentLocation
	# split the commands for main & sub-commands & eventually flags
	cmd = cmd.split()
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
	os.system('cls')
	
def cmd_show_progress(cmd):
	'''
	show the current progress for all levels and !for a specific level!

	cmd: the command as a list ['show-progress'] or ['show-progress', '2'] -> for displaying progress of level 2

	no returns
	'''
	global progress, conf
	# itirate over all levels that exists in in the config file
	for i in conf.levels:
		# if the file data/level[number].dat doesn't exists it means that the level is never started or corrupted
		if not os.path.isfile('data/level{}.dat'.format(str(i))):
			continue
		# initiate a level class, that loads all variable needed for determening progress
		tmp = core.study.level('data/level{}'.format(str(i)))
		# print the progress
		print("your progress in level {}: {} left, {} mastered, {} needs review".format(str(i),
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
	if len(cmd) < 2:
		err("incorrect usage of command 'set-level', try 'help set-level' for more information")
		return
	print('Setting current level to level {}'.format(cmd[1]))
	# the param should be numeric
	if not cmd[1].isnumeric():
		err('no such level found: {}'.format(cmd[1]))
	# the param should be an existing level number
	if int(cmd[1]) in conf.levels:
		conf.curr = int(cmd[1])
	else:
		err('no such level found: {}'.format(cmd[1]))


def cmd_start_study(cmd):
	'''
	start the current level or start a specific level

	cmd: the command as a list ['start'] or ['start', 'level's number']

	no returns
	'''
	global progress, conf
	# starting a specific level means setting it first & start it normally
	if len(cmd) > 1:
		cmd_setLevel(['set-level', cmd[1]])
	print('Starting level {}'.format(str(conf.curr)))
	# load the level class of the level
	progress = core.study.level("data/level" + str(conf.curr))
	# check if the level is already mastered & prompt the user for restuding it 
	if check_completed():
			echo('this level is already completed, do uyou want to restudy it? (y|n):')
			res = input()
			if res == 'y':
				progress.reset()
			else:
				print('Please use set-level command to choose the level you want')
				return
	print("choose the right answer or type end to goback to study\n")
	# this ans have no meaning at all just to start the while
	ans = 'no meaning at all'
	while ans != "end":
		# get a word randomley from the levels database
		w = progress.getWord()
		# print the choices nicely 
		core.printWord(w)
		ans = input("you choose: ")
		print()
		# 'blank' means i don't know, a number is expected or end command. if not pass to the next question
		if (not ans.isnumeric()) and ans!="":
			if not ans == 'end':
				echo('choose the right answer or type end to goback to study -- PASSING TO NEXT QUESTION\n')
			continue
		# check if the answer is correct
		if(ans == '' or ans == str(len(w[1][1])) or w[1][1][int(ans)] != w[1][2]):
			progress.addNeedsReview(w[0])
			echo("not correct ! it means {} \n".format(w[1][2]))
		else:
			progress.addMastered(w[0])
			if check_completed():
				level_completed()
				break
			echo("correct, {} means {} \n".format(w[1][0], w[1][2]))
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
	core.parser.parse(cmd[1], "data/level" + str(len(conf.levels)))
	# if no level is set as the current level, set this level as the current level
	if conf.curr == -1:
		conf.curr = len(conf.levels)
	print("level has been added successfully")
	# add this level to the config file
	conf.levels += [len(conf.levels)]
	# initiate the level
	tmp = core.study.level("data/level" + str(conf.levels[-1]))
	del tmp

def cmd_show(cmd):
	'''
	show current levels

	cmd: the command as list ['show-levels'] expected

	no returns
	'''
	global conf
	for i in conf.levels:
		print('Level {}'.format(str(i)))	

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
	return len(progress.mastered) == len(progress.choices)

def level_completed():
	'''
	the command to execute if level is completed

	no returns
	'''
	print('----------------- !! great work !! -----------------')
	print('level {} is completed'.format(str(conf.curr)))
	# check if there is a level ahead
	if max(conf.levels) > conf.curr:
		for i in conf.levels:
			if i > conf.curr:
				# prompt the user if he wants to pass to next level, otherwise he needs to choose a level himself
				echo('Do you wanna pass to level {} (y|n):'.format(str(i)))
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
	global currentLocation
	print("\n", currentLocation, ": ", end='', sep="")
	if curr() == 'study':
		echo('<Current level: level{}> '.format(str(conf.curr)))
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

# main loop
while(exitCode == 0):
	initCmd()

# save the config file if everything goes normally
conf.save()

echo("\nexited with code " + str(exitCode))
