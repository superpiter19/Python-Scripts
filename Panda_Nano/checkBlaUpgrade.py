import sys
import os.path

def compareList(l152,l20):
	#El 2 campo (Infodiscard debe ser distinto en los ficheros). Los demas iguales y ademas el fichero de 20 tiene dos campos mas
	bCompare = True
	if ((len(l152) != 18) or (len(l20) != 20)):
		bCompare = False
	
	if (bCompare):
		for i in range(18):
			if (i == 1):
				if (l152[i] == l20[i]):
					bCompare = False
					break
			else:
				element152 = l152[i]
				if (i == 17):
					element152 = l152[i].split("\n")[0] #Es el ultimo y lleva un salto de linea. Lo elimino
				if (element152 != l20[i]):
					bCompare = False
					break	
	return bCompare
	
def validateArgs(args):
	bReturn = False
	sPath152 = sPath20 = None
	if (len(args) == 2):
		sPath152 = sys.argv[1] + "\\out_152.txt"
		sPath20 = sys.argv[1] + "\\out_20.txt"
		if (os.path.exists(sPath152) and os.path.exists(sPath20)):
			bReturn = True
	return bReturn,sPath152,sPath20

#El script recibe como parametro el path donde se almacenaran los ficheros de log del upgrade de la cuarentena
bOk,sPath152,sPath20 = validateArgs(sys.argv)
if (not bOk):
	print("Error Parametros incorrectos. Uso <py> <path de ficheros de upgrade>")	
else:	
	bRightUpgrade = True
	file152 = open(sPath152,"r")
	file20 = open(sPath20,"r")
	line152 = file152.readline();
	line20 = file20.readline();
	while (line152 and line20 and bRightUpgrade):
		l152 = line152.split("|")
		l20 = line20.split("|")
		bRightUpgrade = compareList(l152,l20)
		line152 = file152.readline();
		line20 = file20.readline();
	
	if (line152 or line20):
		bRightUpgrade = False
	file152.close()
	file20.close()
	print(bRightUpgrade)
