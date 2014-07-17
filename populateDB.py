# Key
# 0:system, 1:status, 2:sysvercount, 3:description, 4:sysver, 5:fullname
# 6:domain, 7:jreversion, 8:license, 9:distribution, 10:releasedate
# 11:sourcepackages, 12:n_bin, 13:n_both, 14:n_files, 15:n_top(bin), 16:loc(both), 
# 17:ncloc(both), 18:url

import sqlite3
import itertools
import qualitas

SysID = itertools.count(1)
VersID = itertools.count(1)

conn = sqlite3.connect('%s/Systems.db' % qualitas.getDBName())
c = conn.cursor()

systems = {}
header = True

# can open summary.csv from e, f, or r; they are all identical
with open('%s/metadata/summary.csv' % qualitas.getDirName()) as f:
	for line in f:
		if line[0] == '#':
			continue
		if header:
			header = False
			continue

		cols = line.split('\t')

		if cols[0] not in systems:
			systems[cols[0]] = SysID.next()
		
			tmp = (systems[cols[0]], cols[0], cols[1], cols[3], cols[5], cols[6], cols[2])
			c.execute('INSERT INTO Systems VALUES (?,?,?,?,?,?,?)', tmp) 
			
		vid = VersID.next()
		tmp = (vid, systems[cols[0]], cols[4], cols[7], cols[8], cols[9], cols[10], cols[12], cols[13],
				 cols[14], cols[15], cols[16], cols[17], cols[18])
		c.execute('INSERT INTO Versions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tmp)
		
		packs = [ (vid, p, ) for p in cols[11].split(' ')]
		c.executemany('INSERT INTO SourcePackages VALUES (?,?)', packs)

conn.commit()
conn.close()