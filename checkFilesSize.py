import sys
import os
import time
import win32api
import win32con

'''
REcorre el directorio pasado y muestra los ficheros que superen el tamano en MB indicado
'''

def validateArgs(args):
	bRet = False
	sPath = None
	iSize = 0
	if (len(args) == 3):
		sPath = args[1]
		iSize = int(args[2]) * 1000 * 1000
		if (os.path.exists(sPath)):
			bRet = True
		print(sPath,iSize)
	return bRet,sPath,iSize
	
#MAIN

bArgs,sDir,iMinSize = validateArgs(sys.argv)
if (bArgs):	
	listFiles = {}
	for root, dirs, files in os.walk(sDir):
		for f in files:
			fullpath = os.path.join(root, f)
			if (win32api.GetFileAttributes(fullpath) & win32con.FILE_ATTRIBUTE_ARCHIVE):
				fileSize = os.path.getsize(fullpath)
				if (fileSize > iMinSize):
					print("{0} Size={1}".format(fullpath,fileSize))
			
else:
	print("Error en params uso: <py> <directorio_ficheros> <tamano minimo en MB para mostrar ficheros>")