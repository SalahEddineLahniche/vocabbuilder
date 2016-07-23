import core
import core.parser


currentLocation = "master"
dirs = ["study", "game"]
exitCode = 0
        

def exc(cmd):
	global currentLocation
	cmd = cmd.split(" ")
	if(cmd[0] == "exit"):
		exit()
	if(curr() == "master"):
		if(cmd[0] == "goback"):
			echo("where the hell u wanna go back !\n")
		elif(cmd[0] == "goto"):
			if(len(cmd) < 2):
				echo("error: section not recognized\n")
				return
			if(cmd[1] not in dirs):
				echo("error: section not recognized\n")
				return
			addLevel(cmd[1])
	if(curr() == "study"):
		if(cmd[0] == "goback"):
			goBack()
	if(curr() == "game"):
		if(cmd[0] == "goback"):
			goBack()
		

def initCmd():
	global currentLocation
	print(currentLocation, ": ", end='')
	exc(input())

def echo(string):
	print(string, end='')

def addLevel(level):
	global currentLocation
	currentLocation += " $ " + level

def curr():
	global currentLocation
	return currentLocation.split(" $ ")[-1]

def goBack():
	global currentLocation
	tmp = currentLocation.split(" $ ")
	tmp.pop()
	currentLocation = " $ ".join(tmp)

def exit():
	global exitCode
	exitCode = 1


while(exitCode == 0):
	initCmd()

echo("\nexited with code " + str(exitCode))
