import core
import core.parser
import core.study
import core.game
import os
import os.path


currentLocation = "master"
sections = ["study", "game", "master"]
globalCmds = ["goto", "exit", "goback", "help"]
masterCmds = ['add-level', 'show-levels']
studyCmds = ['start', 'set-level', 'show-progress', 'show-levels']
gameCmds = []
exitCode = 0
        

def exc(cmd):
	global currentLocation
	cmd = cmd.split(" ")
	if(cmd[0] == "exit"):
		cmd_exit()
	elif(cmd[0] == "goback"):
		cmd_goback()
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
def cmd_show_progress(cmd):
	global progress, conf
	for i in conf.levels:
		if not os.path.isfile('data/level{}.dat'.format(str(i))):
			continue
		tmp = core.study.level('data/level{}'.format(str(i)))
		print("your progress in level {}: {} left, {} mastered, {} needs review".format(str(i),
			str(len(tmp.wordsleft)), str(len(tmp.mastered)), str(len(tmp.needsReview))))
		del tmp


def cmd_setLevel(cmd):
	global conf
	if len(cmd) < 2:
		err("incorrect usage of command 'set-level', try 'help set-level' for more information")
		return
	print('Setting current level to level {}'.format(cmd[1]))
	if not cmd[1].isnumeric():
		err('no such level found: {}'.format(cmd[1]))
	if int(cmd[1]) in conf.levels:
		conf.curr = int(cmd[1])
	else:
		err('no such level found: {}'.format(cmd[1]))


def cmd_start_study(cmd):
	global progress, conf
	if len(cmd) > 1:
		cmd_setLevel(['set-level', cmd[1]])
	print('Starting level {}'.format(str(conf.curr)))
	progress = core.study.level("data/level" + str(conf.curr))
	if check_completed():
			echo('this level is already completed, do uyou want to restudy it? (y|n):')
			res = input()
			if res == 'y':
				progress.reset()
			else:
				print('Please use set-level command to choose the level you want')
				return
	print("choose the right answer or type end to goback to study\n")
	ans = 'no meaning at all'
	while ans != "end":
		w = progress.getWord()
		core.printWord(w)
		ans = input("you choose: ")
		print()
		if (not ans.isnumeric()) and ans!="":
			if not ans == 'end':
				echo('choose the right answer or type end to goback to study -- PASSING TO NEXT QUESTION\n')
			continue
		if(ans == '' or ans == str(len(w[1][1])) or w[1][1][int(ans)] != w[1][2]):
			progress.addNeedsReview(w[0])
			echo("not correct ! it means {} \n".format(w[1][2]))
		else:
			progress.addMastered(w[0])
			if check_completed():
				level_completed()
				break
			echo("correct, {} means {} \n".format(w[1][0], w[1][2]))
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
	core.parser.parse(cmd[1], "data/level" + str(len(conf.levels)))
	if conf.curr == -1:
		conf.curr = len(conf.levels)
	print("level has been added successfully")
	conf.levels += [len(conf.levels)]
	tmp = core.study.level("data/level" + str(conf.levels[-1]))
	del tmp

def cmd_show(cmd):
	global conf
	for i in conf.levels:
		print('Level {}'.format(str(i)))	

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

def cmd_goback(cmd = []):
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
		elif(cmd[1] == "help"):
			print("get the help for the specific command")
		elif(cmd[1] == "add-level" and curr() == "master"):
			print("add a specefic level\n\nuse: add-level [path]\npath: a valid dictionary file")
		elif(cmd[1] == "show-levels"  and curr() == "master"):
			print("show existing levels")
		elif(cmd[1] == "show-progress"  and curr() == "study"):
			print("show current progress for existing levels")
		elif(cmd[1] == "set-level"  and curr() == "study"):
			print("set a level to study\n\nuse: set-level [number]\nthe parameter is the index of level. goback to master then type 'show-levels' to view existing levels")
		else:
			err(cmd[1], "nr")
			print("try '-h' to view all commands")


def check_completed():
	return len(progress.mastered) == len(progress.choices)

def level_completed():
	print('----------------- !! great work !! -----------------')
	print('level {} is completed'.format(str(conf.curr)))
	if max(conf.levels) > conf.curr:
		for i in conf.levels:
			if i > conf.curr:
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
	global currentLocation
	print("\n", currentLocation, ": ", end='', sep="")
	if curr() == 'study':
		echo('<Current: level{}> '.format(str(conf.curr)))
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




def err(strErr, errType=""):
	echo('-!- : ')
	if(errType == "nr"): #not recognized error
		echo(strErr + " is not recognized\n\n")
	elif(errType == ""):
		echo(strErr + "\n\n")




conf = core.config('data/config.dat')
progress = None
while(exitCode == 0):
	initCmd()

conf.save()
echo("\nexited with code " + str(exitCode))
