import os
import sys
import xml.etree.cElementTree as cET

def buscaXMLTag(xmlFile,xmlTag):
	resultList = []
	try:
		tree = cET.parse(xmlFile)
		root = tree.getroot()
		for val in root.findall(xmlTag):			
			print(val.text)
	except:
		print 'xxx El fichero no existe o esta mal formado.'
		print 'xxx Path del fichero: ' + xmlFile
		print 'xxx Etiqueta sobre la que se realizo la busqueda: ' + xmlTag
	
if (len(sys.argv) != 2):
	print("Error. py xmlFile")
else:
	datos = buscaXMLTag(sys.argv[1],"./File/Disk/Path")
	