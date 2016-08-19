import re
import sys
import getopt

r = re.compile('(MAJOR_VERSION|MINOR_VERSION|PUBLISH|BUILD) = (\d+)')

major = False
minor = False
publish = False
build = False

opts, args = getopt.getopt(sys.argv[1:],'mpb' ,['major', 'minor', 'publish', 'build'])

for o, a in opts:
	if o in ('--major'):
		major = True
	elif o in ('-m', '--minor'):
		minor = True
	elif o in ('-p', '--publish'):
		publish = True
	elif o in ('-b', '--build'):
		build = True

f = open('core/predef.py', 'r')
src = f.read()
f.close()

def replace(match):
	global major, minor, publish, build
	v = 0
	if match.group(1) == 'MAJOR_VERSION' and major:
		v = int(match.group(2)) + 1
		return match.group(1) + ' = ' + str(v)
	if match.group(1) == 'MINOR_VERSION' and minor:
		v = int(match.group(2)) + 1
		return match.group(1) + ' = ' + str(v)
	if match.group(1) == 'PUBLISH' and publish:
		v = int(match.group(2)) + 1
		return match.group(1) + ' = ' + str(v)
	if match.group(1) == 'BUILD' and build:
		v = int(match.group(2)) + 1
		return match.group(1) + ' = ' + str(v)
	return match.group(0)

src = r.sub(replace, src)

f = open('core/predef.py', 'w')
f.write(src)
f.close()

