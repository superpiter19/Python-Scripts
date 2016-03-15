import os
from win32com.shell import shell, shellcon
import msvcrt as keys

lDrives = ['C:','D:']

keys.getch()
for drive in lDrives:
	#print(drive)
	print (shell.SHQueryRecycleBin(drive))

print (shell.SHQueryRecycleBin(None))