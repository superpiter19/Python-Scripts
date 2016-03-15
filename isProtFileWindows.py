import win32file
import sys
import os

def validateArgs(args):
	bRet = False
	sFilePath = None
	if (len(args) == 2):
		sFilePath = args[1]
		if (os.path.exists(sFilePath)):
			bRet = True
	
	return bRet,sFilePath
	

'''Main'''
bRet,sFPath = validateArgs(sys.argv)

if (bRet):
	bRet = win32file.SfcIsFileProtected(sFPath)
	print("{0} protegido por Windows:{1}".format(sFPath,bRet))
else:
	print("Error. Uso py <nombre de fichero>")