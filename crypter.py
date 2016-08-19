def padLeft(s, n):
	if len(s) < n:
		s = '0'*(n - len(s)) + s
	return s


def crypt(s):
	c = ''
	for i in s:
		n = ord(i)
		n = hex(n)
		n = n[2:]
		n = padLeft(n, 2)
		c += n
	return c

def decrypt(s):
	import re
	r = re.compile('..')
	l = r.findall(s)
	d = ''
	for i in l:
		o = int(i, 16)
		o = chr(o)
		d += o
	return d


