import md5
import sys
import os
import win32api
import win32con
import subprocess
import shutil

'''
GLOBALES
'''
def validateArgs(args):
	bRet = False
	sPath = LIBRE_OFFICE_PATH = CALIBRE_PATH = None
	bOnlyCalibre = False
	
	print(args[2])
	if ((len(args) == 2) or ((len(args) == 3) and (args[2].lower() == "onlycalibre"))):
		sPath = args[1]
		if (os.path.exists(sPath)):
			bRet = True
		if (len(args) == 3):
			#Usar solo el calibre para convertir de pdf a mobi
			print("Usar solo el calibre")
			bOnlyCalibre = True
	else:
		print("Error en parametros. Uso: <exe> <directorioFicheros> OPT [onlyCalibre]")
			
	HKLMKey = win32api.RegConnectRegistry(None, win32con.HKEY_LOCAL_MACHINE)							
	if (bRet):
		#Se comprueba si esta instalado Calibre
		try:
			hKeyCalibre = win32api.RegOpenKey(HKLMKey,"SOFTWARE\\calibre\\Installer")
			CALIBRE_PATH = win32api.RegQueryValueEx(hKeyCalibre,"InstallPath")[0]
			CALIBRE_PATH += "calibre.exe"			
			print("Path Calibre: {0}".format(CALIBRE_PATH))
		except:
			print("No tienes instalado el calibre")
			bRet = False
		
		if (bRet):
			hKeyCalibre.Close()
	
	if (bRet and not bOnlyCalibre):
		#Se comprueba si esta instalado LibreOffice
		try:
			hKeyLibreOffice = win32api.RegOpenKey(HKLMKey,"SOFTWARE\\LibreOffice\\LibreOffice\\4.2")
			LIBRE_OFFICE_PATH = win32api.RegQueryValueEx(hKeyLibreOffice,"Path")[0]
			print("Path LibreOffice: {0}".format(LIBRE_OFFICE_PATH))
		except:
			print("No tienes instalado el LibreOffice 4.2 Si tienes otro cambia este puto script. Estos linuxeros no saben hacer una instalacion generica en el registro de windows...")
			bRet = False
		
		if (bRet):
			hKeyLibreOffice.Close()
	
	HKLMKey.Close()
			
	return bRet,sPath,CALIBRE_PATH,LIBRE_OFFICE_PATH,bOnlyCalibre

	
def convertDocToPdf(docFullPath,outDir,LOfficePath):
	print("LibreOffice")
	subprocess.call([LOfficePath,"--headless","--convert-to", "pdf","--outdir",outDir,docFullPath])
	
def convertPdfToMobi(pdfFullPath,outDir,CalibrePath):
	tpAux = pdfFullPath.split('.')[0].split('\\')
	MobiFileName = out_dir + "\\" + tpAux[len(tpAux) - 1] + ".mobi"
	print(MobiFileName)
	posLastSlash = CalibrePath.rfind("\\")
	ebookConvertPath =  CalibrePath[:posLastSlash + 1] + "ebook-convert.exe"
	print(ebookConvertPath)
	subprocess.call([ebookConvertPath,pdfFullPath,MobiFileName])
'''
Utiliza libreoffice para convertir de Doc a pdf y calibre para convertir de pdf a mobi.
'''

bArgs,sDir,CalibrePath,LOfficePath,bOnlyCalibre = validateArgs(sys.argv)
if (bArgs):
	out_dir = os.path.abspath(os.path.curdir) + "\\ConvertedFiles"
	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)	
	
	
	root_len = len(os.path.abspath(sDir))		
	for root, dirs, files in os.walk(sDir):
		archive_root = os.path.abspath(root)[root_len:]
		for f in files:
			#Si la extension del fichero es Doc
			tuple_extension = f.split('.')
			file_extension = tuple_extension[len(tuple_extension) - 1]
			fullpath = os.path.join(root, f)					
			if (not bOnlyCalibre):
				if (("doc" == file_extension.lower()) or ("docx" == file_extension.lower())):
					convertDocToPdf(fullpath,out_dir,LOfficePath)
			else:
				#se copian todos los pdf a la ruta de ficheros convertidos
				if ("pdf" == file_extension.lower()):
					shutil.copyfile(fullpath,out_dir + "\\" + f)
	
	
	#conversion a mobi. Hay que darle un tiempo a la conversion a pdf
	root_len = len(os.path.abspath(out_dir))		
	for root, dirs, files in os.walk(out_dir):
		archive_root = os.path.abspath(root)[root_len:]
		for f in files:
			#Si la extension del fichero es Doc
			tuple_extension = f.split('.')
			file_extension = tuple_extension[len(tuple_extension) - 1]
			if ("pdf" == file_extension.lower()):
				fullpath = os.path.join(root, f)
				convertPdfToMobi(fullpath,out_dir,CalibrePath)
			
			
			
	

