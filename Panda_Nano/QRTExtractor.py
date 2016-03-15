import os
import sys
import zipfile
import subprocess
import gzip
import shutil

def validateArgs(args):
	bRet = False
	sQrtDir = sOutDir = None
	if (len(args) == 3):
		sQrtDir = args[1]
		sOutDir = args[2]
		if (os.path.exists(sQrtDir) and os.path.exists(sOutDir)):
			bRet = True
	
	return bRet,sQrtDir,sOutDir

def extractZipFiles(extractDir,filePath,fName):
	zipContent = zipfile.ZipFile(filePath,"r")
	filePath = extractDir + "\\" + fName
	if (not os.path.exists(filePath)):
		os.mkdir(filePath)
	for fZipName in zipContent.namelist():
		fileTempName = filePath + "\\" + fZipName
		if ("QEINFO" == fZipName):
			fileTempName = fileTempName + ".xml"			
		fileContent = zipContent.read(fZipName)
		fTemp = open(fileTempName,"wb")
		fTemp.write(fileContent)
		fTemp.close()
	zipContent.close()

def extractGZipFiles(extractDir,QEPath,dirName):
	'''
	En dirName se recibe el directorio de un QE determinado
	'''
	extractFilePath = extractDir + "\\" + dirName
	if (not os.path.exists(extractFilePath)):
		os.mkdir(extractFilePath)
	QEFileList = os.listdir(QEPath)
	for fName in QEFileList:	
		szOutFileName = extractFilePath + "\\" + fName
		fileName = QEPath + "\\" + fName 
		cmpFile = gzip.open(fileName, "r");
		fileContent = cmpFile.read();
		fOut = open(szOutFileName,"wb")
		fOut.write(fileContent)
		fOut.close()
		cmpFile.close()
			
def desencryptFiles(encryptedFilesDir):
	'''
	Cada fichero de este directorio esta encryptado. Se llama a testdecrypt para desencriptarlo
	'''
	dirList = os.listdir(encryptedFilesDir)
	for dirName in dirList:
		#Cada elemento es un directorio donde estan los ficheros del QE
		subDirName = encryptedFilesDir + "\\" + dirName
		fileList = os.listdir(subDirName)
		for fEncName in fileList:
			szEncPath = subDirName + "\\" + fEncName
			testDecryptPath = os.curdir + "\\TesterCrypt.exe" 
			subprocess.call([testDecryptPath,"d",szEncPath])		
		
	
def extractDirFiles(fileDir,outDir,zipType):
	'''
	Se recorre el directorio de entrada, se descomprimen los ficheros y se vuelcan en el directorio de salida
	'''
	fileList = os.listdir(fileDir)
	for fName in fileList:
		szPath = fileDir + "\\" + fName
		if ("zip" == zipType):
			extractZipFiles(outDir,szPath,fName)
		elif("gzip" == zipType):
			extractGZipFiles(outDir,szPath,fName)
	
	return len(fileList)
#Main
bValidArgs,szQrtDir,szOutDir = validateArgs(sys.argv)
if (bValidArgs):
	fileList = os.listdir(szQrtDir)
	tempDir = szOutDir + "\\Tmp"
	if (not os.path.exists(tempDir)):
		os.mkdir(tempDir)
	#Se sacan los ficheros del zip inicial
	numQEs = extractDirFiles(szQrtDir,tempDir,"zip")	
	#se desencriptan todos los ficheros
	desencryptFiles(tempDir)
	#se extraen todos los ficheros gzip al directorio de salida
	extractDirFiles(tempDir,szOutDir,"gzip")
	#Se borra el directorio temporal y todo lo que contenga
	shutil.rmtree(tempDir)
	print("\nExtraidos %d QEs"%numQEs)
else:
	print("Error en parametros. py <directorioQuarentena> <Directorio de Salida>. Ambos directorios deben existir")
	
	



