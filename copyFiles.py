# -*- coding: latin-1 -*-
import sys
import os
import time
import win32api
import win32con
import shutil

'''
Recibe 3 parámetros un directorio con ficheros, un directorio de destino y un entero n.
Realiza n copias de los ficheros del directorio origen en otro directorio que se crea con nombre copyDir1,copuDir2...copyDirn en el directorio de destino
'''

def validateArgs(args):
	bRet = False
	sPath = None
	sDestPath = None
	iNumCopies = 0
	if (len(args) == 4):
		sPath = args[1]
		sDestPath = args[2]
		iNumCopies = int(args[3])
		attrib = win32api.GetFileAttributes(sPath)
		if (not os.path.exists(sPath) or not os.path.exists(sDestPath) or (attrib  & win32con.FILE_ATTRIBUTE_ARCHIVE)):
			print("Alguno de los paths es incorrecto")
		elif (0 >= iNumCopies):
			print("el numero de copias debe ser un numero positivo")	
		else:
			bRet = True	
	else:
		print("Uso: <py> <directorio origen> <directorio destino> <numero de copias>")
	return bRet,sPath,sDestPath,iNumCopies
	
#MAIN
bCorrectArgs,sDir,sDestDir,iNumCopies = validateArgs(sys.argv)
if (bCorrectArgs):
	fileList = []
	for root, dirs, files in os.walk(sDir):
		for f in files:
			fullpath = os.path.join(root, f)
			fileList.append(fullpath)						
	for i in range(iNumCopies):
		completeDestPath = sDestDir + "\\" + "copyDir" + "{0}".format(i)
		if (not os.path.exists(completeDestPath)):
			os.mkdir(completeDestPath)
		else:
			shutil.rmtree(completeDestPath)
			os.mkdir(completeDestPath)
		t0 = time.clock()
		numFiles = 0
		for fullpath in fileList:
			path,fileName = os.path.split(fullpath)
			shutil.copyfile(fullpath,completeDestPath + "\\" + fileName)
			numFiles = numFiles + 1
		tCopy = time.clock() - t0
		print("Copiados {0} Ficheros tiempo: {1} seg".format(numFiles,tCopy))
						
			
			
			
