import md5
import sys
import os

def validateArgs(args):
	bRet = False
	sPath = None
	if (len(args) == 2):
		sPath = args[1]
		if (os.path.exists(sPath)):
			bRet = True
	
	return bRet,sPath
'''
Calcula e imprime por pantalla el md5 de todos los ficheros de un directorio
'''

bArgs,sDir = validateArgs(sys.argv)
if (bArgs):
	root_len = len(os.path.abspath(sDir))
	for root, dirs, files in os.walk(sDir):
		archive_root = os.path.abspath(root)[root_len:]
		for f in files:
			fullpath = os.path.join(root, f)
			print(fullpath)
			fil = open(fullpath,"rb")
			bufferRead = fil.read()
			print("\tMD5:" + md5.new(bufferRead).hexdigest().upper())
			fil.close()
			
	
else:
	print("Error en params uso: <py> <directorio_ficheros>")

