currentLocation = "master"
dirs = ["study", "game"]
        

def exc(cmd):
	global currentLocation
	cmd = cmd.split(" ")
	if(cmd[0] == "-b"):
		if(curr() == "master"):
			echo("where the hell u wanna go back !")
		goBack()
	elif(cmd[0] == "-c"):
		exit()
	elif(cmd[0] == "cd"):
		addLevel(cmd[1])

def initCmd():
	global currentLocation
	print(currentLocation, ": ", end='')
	exc(input())

def echo(string):
	print(string, end='')

def addLevel(level):
	global currentLocation
	currentLocation += " $ " + level
	initCmd()

def curr():
	global currentLocation
	return currentLocation.split(" $ ")[-1]

def goBack():
	global currentLocation
	tmp = currentLocation.split(" $ ")
	tmp.pop()
	currentLocation = " $ ".join(tmp)
	initCmd()

def exit():
	print("\n\n...exited")


initCmd()

