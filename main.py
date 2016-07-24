import core
import core.parser


currentLocation = "master"
sections = ["study", "game"]
globalCmds = ["goto", "exit", "goback", "help"]
masterCmds = []
studyCmds = []
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
	else:
		err(cmd[0], 'nr')
		cmd_help()

		
#Commands
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
		print("try goto study\nor goto game\nor -h to view all commands")
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
			print("specify a command to get help or type -h to show all available commands")
	else:
		if(cmd[1] == "goto"):
			print("go to a specefic section: study or game")
		elif(cmd[1] == "goback"):
			print("go back to master")
		elif(cmd[1] == "exit"):
			print("exit the app")
		elif(cmd[1] == "help"):
			print("get the help for the specific command")





def initCmd():
	global currentLocation
	print("\n", currentLocation, ": ", end='', sep="")
	exc(input())

def echo(string):
	print(string, end='')

def addLevel(level):
	global currentLocation
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


while(exitCode == 0):
	initCmd()

echo("\nexited with code " + str(exitCode))
