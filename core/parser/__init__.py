# def parse(path):
# 	f = open(path)
# 	dico = {}
# 	tmpLine = f.readline()
# 	tmpArray = []
# 	while tmpLine:
# 		if(tmpLine[0] == "#"):
# 			tmpLine = f.readline()
# 			continue
# 		tmpArray = tmpLine.split(";")
# 		dico[tmpArray[0]] = tmpArray[1].split(".")
# 		tmpLine = f.readline()
# 	print(dico)
# 	f.close()


# 		