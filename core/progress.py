def progress_echo(percentage, width = 40):
	p = '['
	r = int((width) * percentage)
	for i in range(r):
		p += "|"
	for i in range(r, width):
		p += " "
	p += "]"
	print(p, end="")
