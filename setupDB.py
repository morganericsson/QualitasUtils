import sqlite3
import qualitas

# Mapped from the Qualitas metadata. 
_constants = [ (4, 0, 'In src pkg (user-defined)'), (4, 1, 'Not in src pkg'), (5, 0, 'Both bin and src'), (5, 1, 'Bin only'), (5, 2, 'Src only'), (6, 0, 'Distributed'), (6, 1, 'Not distributed'), (7, 0, 'Top-level public'), (7, 4, 'Top-level non-public'), (7, 1, 'Top-level different name'), (7, 2, 'Nested'), (7, 3, "Probably haven't seen source"), (7, -1, 'No source, or not parsed') ]

conn = sqlite3.connect('%s/Systems.db' % qualitas.getDBName())
c = conn.cursor()

# _expectedKeys = ['System Version', 'Source Packages', 'Ignore Packages', 'Distributed', 'Source Roots']

c.execute('CREATE TABLE Systems (SysId INTEGER PRIMARY KEY, System TEXT, DevelopmentStatus TEXT, Description TEXT, FullName TEXT, Domain TEXT, NoVers INTEGER)')

c.execute('CREATE TABLE Versions (VersId INTEGER PRIMARY KEY, SysId INTEGER, SystemVersion TEXT, JREVersion TEXT, License TEXT, Distribution TEXT, ReleaseDate TEXT, noBin INTEGER, noBoth INTEGER, noFiles INTEGER, noTopLevelTypesBin INTEGER, LoCBoth INTEGER, NCLoCBoth INTEGER, URL TEXT)')

# is this same as Source Packages in content.csv? Yes (based on sample)
c.execute('CREATE TABLE SourcePackages ( VersId INTEGER, PackagePrefix TEXT )')
c.execute('CREATE TABLE IgnorePackages ( VersId INTEGER, PackagePrefix TEXT )')
c.execute('CREATE TABLE Distributed ( VersId INTEGER, Path TEXT )')
c.execute('CREATE TABLE SourceRoots ( VersId INTEGER, Path TEXT )')


c.execute('CREATE TABLE Files (VersId INTEGER, FQN TEXT, LocBin TEXT, LocSrc TEXT, InSrcPkg INTEGER, "SrcOrBin?" INTEGER, "Distributed?" INTEGER, "Analyzed?" INTEGER, LoC INTEGER, NCLoC INTEGER)')

c.execute('CREATE TABLE Constants (ColId INTEGER, Value INTEGER, Description TEXT, PRIMARY KEY(ColId, Value))')
c.executemany('INSERT INTO Constants VALUES (?,?,?)', _constants)

conn.commit()
conn.close()