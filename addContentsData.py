import sqlite3
import re
import glob
import qualitas


conn = sqlite3.connect('%s/Systems.db' % qualitas.getDBName())
c = conn.cursor()

for f in glob.iglob('%s/Systems/*/*/metadata/contents.csv' % (qualitas.getDirName())):
	d = qualitas.parseContentMD(f)
	
	c.execute('SELECT VersId FROM Versions where SystemVersion = ?', (d['System Version'], ))
	version = c.fetchone()[0]
	
	if len(d['Ignore Packages'].strip()) > 0:
		tmp = [ (version, p) for p in d['Ignore Packages'].split(',')]
		c.executemany('INSERT INTO IgnorePackages VALUES (?,?)', tmp)

	if len(d['Distributed'].strip()) > 0:
		tmp = [ (version, p) for p in d['Distributed'].split(',')]
		c.executemany('INSERT INTO Distributed VALUES (?,?)', tmp)

	if len(d['Source Roots'].strip()) > 0:
		tmp = [ (version, p) for p in d['Source Roots'].split(',')]
		c.executemany('INSERT INTO SourceRoots VALUES (?,?)', tmp)

	tmp = qualitas.parseContentTable(f, version)
	c.executemany('INSERT INTO Files VALUES (?,?,?,?,?,?,?,?,?,?)', tmp)

conn.commit()
conn.close()
