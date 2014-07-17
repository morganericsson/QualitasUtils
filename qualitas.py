import re

home = '/Volumes/Raid/Work/Qualitas/Current'
version = 'Complete-20130901'
distributions = [ 'e', 'f', 'r' ]

_re_metadata = re.compile(r'#(?P<key>[\w\s]+\w)[\s]*:[\s]*(?P<value>[\w\.,/-]*)')

def getDirName(distribution = False):
	return '%s/%s' % (home, version)

def getDBName():
	return '%s' % home

def parseContentMD(fn):
	descr = {}
	
	with open(fn) as f:
		inHeader = True
		for line in f:
			if line[0] == '#' and inHeader:
				if line == '#\n':
					inHeader = False
					continue

				m = _re_metadata.match(line)
				if m:
					descr[m.group('key')] = m.group('value')
					continue
	return descr
	
def parseContentTable(fn, vid):
	rows = []
	
	with open(fn) as f:
		for line in f:
			if line[0] == '#':
				continue
			row = line.split('\t')
			if len(row) == 9:				
				if len(row[2].split(',')) > 1:
					for f in row[2].split(','):
						rows.append(tuple([vid] + row[0:2] + [f] + row[3:]))
				else:
					rows.append(tuple([vid] + row))

		return rows