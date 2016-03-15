import sys
import os
import glob

if (len(sys.argv) != 3):
	print("Uso <py> <nombre de fichero a modificar> <numero de modificaciones>")
else:
	fOrig = open(sys.argv[1],"rb")
	i = 0
	dir = os.curdir + "\\modification"
	if not os.path.isdir(dir):
		os.mkdir(dir)
	path,fileName = os.path.split(sys.argv[1])
	tpSplitName = fileName.split(".")
	name = tpSplitName[0]
	if (len(tpSplitName) > 1):
		fBaseExtension = tpSplitName[1]
	baseFileName = dir + "\\" + name
	buffer = fOrig.read()
	
	for i in range(int(sys.argv[2])):
		sufix = "_{0}".format(i)
		fName = baseFileName + sufix
		for w in tpSplitName[1:]:
			fName = fName + "." + w
		fCopy = open(fName,"wb")
		fCopy.write(buffer)
		fCopy.seek(96)
		fCopy.write(sufix)
		fCopy.close()
		
	fOrig.close()
	