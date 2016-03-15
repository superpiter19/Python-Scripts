import win32com.client
import sys

def validateArgs(args):
	bRet = False
	operation = itemID = valueList = listType = profileID = None
	if ((len(args) == 4) or (len(args) == 6)):
		operation = args[1]
		profileID = int(args[2])
		itemID = int(args[3],16)
		if ("LIST" == operation):
			bRet = True
		elif ("ADD" == operation):
			if (len(args) == 6):
				listType = args[4]
				valueList = args[5].split(",")
				bRet = True
				
	return bRet,operation,profileID,itemID,listType, valueList
	
'''
Obtiene todos los valores de una lista de items y los imprime por pantalla. REcibe el objeto de configuracion, el item y el perfil.
'''
def listItem(cfgObject,profileID,itemID):
	tpValues = cfgObject.Get(profileID,itemID)
	print(tpValues)

'''
Anade items a una lista. REcibe el objeto de configuracon , el item, el perfil, el tipo de los elementos, y una lista con los valores a anadir 
'''
def addItem(cfgObject,profileID,itemID,listType,listToAdd):
	#se obtienen los valores actuales de la lista
	tpValues = cfgObject.Get(profileID,itemID)
	insertList = []
	for value in tpValues:
		insertList.append(value)
	
	if ("STRING" == listType):
		for value in listToAdd:
			insertList.append(value)
	elif ("INT" == listType):
		for value in listToAdd:
			insertList.append(int(value))
	
	cfg.Set(profileID,itemID,insertList)
	
#---------------------------------------------------------------------------------	
#MAIN
#---------------------------------------------------------------------------------

bCorrectParams, operation, profileID, itemID, listType, valueList = validateArgs(sys.argv)

if (bCorrectParams):
	#Create NDKApplicationContext
	appCtx = win32com.client.Dispatch("NdkApi.NDKApplicationContext")
	appCtx.Initialize("appconfig.xml")
	# Create 'Ndk.Configuration'
	cfg = appCtx.Get("Ndk.Configuration")
	
	if ("LIST" == operation):
		listItem(cfg,profileID,itemID)
	elif ("ADD" == operation):
		addItem(cfg,profileID,itemID,listType,valueList)
		
	
else:
	print("Error en parametros")
	print("Uso: ConfigureList.py <operation> <profileID> <itemID> [listType] [value] donde:")
	print("<operation> --> Es la operacion a realizar:")
	print("\tLIST --> Muestra por pantalla el contenido del item")
	print("\tADD --> Anade a la lista los valores del parametro [value]")
	print("<profileID> --> identificador numerico del perfil a utilizar")
	print("<itemID> --> identificador en hexadecimal del item")
	print("[listType] --> (Solo para ADD) Tipo de los elementos de la lista:")
	print("\tINT --> Lista de enteros")
	print("\tSTRING --> Lista de cadenas")
	print("[value] --> (Solo para ADD) valores, separados por comas, a anadir a la lista")
	


