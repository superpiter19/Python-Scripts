# -*- coding: latin-1 -*-
import sys
import os
import time
import win32api
import win32con
import shutil
import re
import subprocess

'''
Obtiene todos los ficheros de configuración que hay en una ruta determinada y llama a BuildCfg.exe para crear el dat para el producto.
Hay que tener en cuenta que hay ficheros que no se pueden crear usando el BuildCfg. Habrá que excluirlos explicitamente porque BuildCfg no 
devuelve ningún error.
'''

def validateArgs(args):
	bRet = False
	sPath = None
	sDestPath = None
	if (len(args) == 2):
		sPath = args[1]
		bRet = True
	else:
		print("Uso: <py> <directorio origen> <directorio destino> <numero de copias>")
	return bRet,sPath
	
	

def isXMLNanoConfig(fileName):
	bRet = False
	extension = os.path.splitext(fileName)[1].lower()
	path,name = os.path.split(fileName)
	name = name.split(".")[0]		
	if ((".xml" == extension) and (len(name) == 8) and (re.match("[0-9A-Fa-f]{8}",name))):
		bRet = True
	return bRet
	
def createNanoDat(xmlFile):
	destPath = ".\\NanoCfgFiles"
	exePath = os.curdir + "\\BuildCfg.exe"
	params = "-OID "
	if (not os.path.exists(destPath)):
		os.mkdir(destPath)
		
	path,fileName = os.path.split(xmlFile)
	name = fileName.split(".")[0]
	#el buildcfg exige que el nombre del xml sea buildcfg.xml
	shutil.copyfile(xmlFile,os.curdir + "\\" + "BuildCfg.xml")
	#Se llama a Buildcfg.exe para realizar la conversión
	params = params + name
	subprocess.call([exePath,params])
	#Se deja el dat en el directorio de salida y se borra el xml
	datName = os.curdir + "\\" + name + ".dat"
	if os.path.exists(datName):
		shutil.copyfile(datName,destPath + "\\" + name + ".dat")
	os.remove(datName)	
	
	
	
#MAIN
bOk,sOrigDir = validateArgs(sys.argv)
if bOk:
	i = 0
	for root, dirs, files in os.walk(sOrigDir):
		for f in files:
			fullpath = os.path.join(root, f)
			if isXMLNanoConfig(fullpath):
				i = i + 1
				print(fullpath)
				createNanoDat(fullpath)
	print("Numero de ficheros de configuración de Nano: {0}".format(i))
			