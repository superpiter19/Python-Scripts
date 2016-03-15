import sys
import os
import time

MAX_TIME = 3600 * 24 * 3
	
def validateArgs(args):
	bRet = False
	sPath = None
	if (len(args) == 2):
		sPath = args[1]
		if (os.path.exists(sPath)):
			bRet = True
	
	return bRet,sPath
	
def addFile(list,fileName):
	bNewFile = False
	bCopyFile = False
	extension = os.path.splitext(fileName)[1].lower()
	modTime = os.path.getmtime(fileName)
	creationTime = os.path.getctime(fileName)
	if ( (time.time() - modTime) < MAX_TIME):
		bNewFile = True
	if (creationTime > modTime):
		bCopyFile = True
		
	stExtData = [0,0,0,0]
	if (extension in list.keys()):
		stExtData = list[extension]
		
	stExtData[0] = stExtData[0] + 1
	if (bNewFile):
		stExtData[2] = stExtData[2] + 1
	else:
		stExtData[1] = stExtData[1] + 1
	if (bCopyFile):
		stExtData[3] = stExtData[3] + 1
		
	list[extension] = stExtData
	
def printData(list):
	totalFiles = 0
	for key in list:
		stExtData = list[key]
		data = key + "\tTotal: {0} ".format(stExtData[0]) +  "Nuevos: {0} ".format(stExtData[1]) + "Viejos: {0} ".format(stExtData[2]) + "Copias: {0} ".format(stExtData[3])
		totalFiles = totalFiles + stExtData[0]
		print(data)
	
	print("Total de Ficheros:{0}".format(totalFiles))
'''
{ext:[numeroFicheros,Antiguos,Nuevos,Copias]}
'''

bArgs,sDir = validateArgs(sys.argv)
if (bArgs):	
	listFiles = {}
	for root, dirs, files in os.walk(sDir):
		for f in files:
			fullpath = os.path.join(root, f)
			addFile(listFiles,fullpath)						
	printData(listFiles)
else:
	print("Error en params uso: <py> <directorio_ficheros>")