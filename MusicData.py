import sys
import os
import time
import eyed3

MAX_TIME = 3600 * 24 * 3

C_MUSIC_EXTENSIONS = ["mp3", "wma"]
	
def validateArgs(args):
	bRet = False
	sPath = None
	if (len(args) == 2):
		sPath = args[1]
		if (os.path.exists(sPath)):
			bRet = True
	
	return bRet,sPath
	
def addFile(fileName):
	tag = eyeD3.Tag()
	extension = (os.path.splitext(fileName)[1].lower()).split('.')[1]	
	if(extension in C_MUSIC_EXTENSIONS):
		tag.link(fileName)   
		print(tag.getArtist(), tag.getAlbum(), tag.getTitle())
		return True
	else:
		return False
	
bArgs,sDir = validateArgs(sys.argv)
numMusicFiles = 0
numOtherFiles = 0

if (bArgs):	
	for root, dirs, files in os.walk(sDir):
		for f in files:
			fullpath = os.path.join(root, f)
			if(addFile(fullpath)):
				numMusicFiles = numMusicFiles + 1
			else:
				numOtherFiles = numOtherFiles + 1
	print("Numero de ficheros musicales: {0}".format(numMusicFiles))
	print("Numero de otros ficheros: {0}".format(numOtherFiles))
	
else:
	print("Error en params uso: <py> <directorio_ficheros>")