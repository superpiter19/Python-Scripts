import sqlite3
import os
import sys
from operator import itemgetter

g_jugadores = ["Piter", "Gustavo", "Kitos", "David", "Mian", "Pado", "Rafa", "Sanfe", "Richal", "Jota", "Pablo"]
g_titulos = [1,1,5,2,0,0,0,0,1,0,0]
g_cucharaMadera = [0,0,0,0,0,2,1,1,1,1,3]
g_trofeosVeraniegos = [0,0,0,0,1,0,0,1,0,0,0]
g_historicoPuntos = [4994,5457,5716,4968,4569,4545,3176,4790,4776,3031,0]
g_dataBaseName = "Comunio.db"
g_numJornadas = 50
g_resultDir = ".\\Jornadas"
g_PunishIncrement = 20
g_maxPunish = g_PunishIncrement * (len(g_jugadores) - 1)
g_resultsFileName = "Results.csv"
g_resultsFile = None 

'''
SELECT TJugador.name, TJornada.name, TPuntuacion.puntos, TPuntuacion.pasta, TPuntuacion.prima FROM TJugador,TJornada JOIN TPuntuacion 
ON (TJugador.id = TPuntuacion.jugadorID AND (TJugador.id == 1) AND (TJornada.id == 1))
'''

def createDataBase():
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	conn.execute('pragma foreign_keys=ON')
	# Create tables
	c.execute('''CREATE TABLE TJugador (id INTEGER PRIMARY KEY AUTOINCREMENT,name text NOT NULL UNIQUE, puntos INTEGER NOT NULL, pasta INTEGER NOT NULL, titulos INTEGER NOT NULL, historicoPuntos INTEGER NOT NULL, cucharas INTEGER NOT NULL, trofeos INTEGER NOT NULL, parciales INTEGER NOT NULL)''')
	c.execute('''CREATE TABLE TJornada
             (id INTEGER PRIMARY KEY AUTOINCREMENT,name text NOT NULL UNIQUE, completed INTEGER NOT NULL CHECK (completed IN (0,1)))''')
	c.execute('''CREATE TABLE TPuntuacion
			(id INTEGER PRIMARY KEY AUTOINCREMENT, jugadorID INTEGER NOT NULL, jornadaID INTEGER NOT NULL, puntos INTEGER NOT NULL, pasta INTEGER NOT NULL, 
			FOREIGN KEY(jugadorID) REFERENCES TJugador(id), FOREIGN KEY(jornadaID) REFERENCES TJornada(id) ) ''')
	
	#Insertar jugadores
	pos = 0
	for player in g_jugadores:
		c.execute("INSERT INTO TJugador(name, puntos, pasta, titulos, historicoPuntos, cucharas, trofeos, parciales) VALUES (?, 0, 0, ?, ?, ?, ?, 0)", [player, g_titulos[pos], g_historicoPuntos[pos], g_cucharaMadera[pos], g_trofeosVeraniegos[pos]])
		pos = pos + 1
	#Jornadas
	for i in range(g_numJornadas):
		name = "JORNADA {0}".format(i + 1)
		c.execute("INSERT INTO TJornada(name, completed) VALUES (?,0)", [name])
		
	conn.commit()
	conn.close()
	conn.close()
	
def isDayPrevioslyLoaded(strDay):
	bRet = True
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	idJornada = 0
	
	c.execute('SELECT * FROM TJornada WHERE name=?', [strDay])
	result = c.fetchall()
	if (len(result) == 1):
		reg = result[0]
		completed = (int(reg[2]) == 1)
		if(not completed):
			bRet = False		
		else:
			idJornada = int(reg[0])
	else:
		print("Error en nombre de jornada. {0} {1}".format(strDay, c.fetchall()))		
		
	conn.close()	
	return bRet, idJornada

def insertIntoDatabase(strDayName, dayResults):
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute('SELECT id FROM TJornada WHERE name=?', [strDayName])
	result = c.fetchall()
	selectedDayId = 0
	if (len(result) > 0):
		selectedDayId = result[0][0]
		partialWinner = 1

		for playerData in dayResults:	
			selectedPlayerId = 0	
			c.execute('SELECT id FROM TJugador WHERE name=?', [playerData[0]])
			selectedPlayerId = c.fetchall()[0][0]
			c.execute("INSERT INTO TPuntuacion(jugadorID, jornadaID, puntos, pasta) VALUES(?, ?, ?, ?)",
			[selectedPlayerId, selectedDayId, playerData[1], playerData[2]])
			#Se actualiza el total en la tabla de jugadores
			c.execute("UPDATE TJugador SET puntos = puntos + ?, pasta = pasta + ?, historicoPuntos = historicoPuntos + ? , parciales = parciales + ? WHERE id = ?",[playerData[1], playerData[2], playerData[1], partialWinner, selectedPlayerId])
			#Solo el primero es el ganador
			partialWinner = 0
			
		c.execute("UPDATE TJornada SET completed = 1 WHERE id = ?",[selectedDayId])
	else:
		print("Error en nombre de jornada en fichero {}".format(strDayName))
	conn.commit()
	conn.close()

def prepareData(jName, dayClassification):
	dayClassification.sort(key=itemgetter(1,3), reverse = True) 	
	pos = 1
	print("Clasificacion {0}".format(jName))
	print("Pos\tNombre\tPuntos\tValor\tPasta")
	g_resultsFile.write("Pos;Nombre;Puntos;Valor;Pasta\n")
	pasta=0
	dataToInsert = []
	totalMoney = 0
	for element in dayClassification:
		if pos > 1:
			pasta = pasta + g_PunishIncrement
		playerMoney = pasta
		#si está sancionado se paga el maximo de pasta y no se dan recompensas por jugadores en once ideal
		if element[2]:
			playerMoney = g_maxPunish					
		print("{0}\t{1}\t{2}\t{3}\t{4}".format(pos, element[0], element[1], element[3], playerMoney/100))
		g_resultsFile.write("{0};{1};{2};{3};{4}\n".format(pos, element[0], element[1], element[3], playerMoney/100))
		totalMoney = totalMoney + playerMoney/100
		pos = pos + 1
		dataToInsert.append((element[0], element[1], playerMoney))
	print("Total Money: {0}".format(totalMoney))
	g_resultsFile.write("TOTAL;;;;;{0};\n".format(totalMoney))
	return dataToInsert
	
def parseResultFile(fullPath, fileName):
	'''
		El fichero tiene 4 columnas
		Nombre_Jugador Puntos_Jornada Sancionado(1,0) Valor_equipo 
	'''
	jName = fileName.split('.')[0] 
	
	bLoaded,idJornada = isDayPrevioslyLoaded(jName)
	if not bLoaded:
		file = open(fullPath, "r")
		buffer = file.read()
		file.close()
		regValues = buffer.split('\n')		
		dayClassification = []
		addedPlayers = []
		for reg in regValues:
			splitReg = reg.split(';')
			print(splitReg)
			if len(splitReg) >= 3:			
				playerName = splitReg[0]
				playerPoints = 0
				playerTeamValue = 0
				try:
					playerPoints = int(splitReg[1])
				except ValueError:
					playerPoints = 0
				playerPunished = False
				if splitReg[2] == "1":
					playerPunished = True
				try:
					playerTeamValue = int(splitReg[3])
				except ValueError:
					playerTeamValue = 0
				if not playerName in g_jugadores:
					print("Error. Jugador Desconocido {0}".format(reg))
				else:
					dayClassification.append((playerName, playerPoints, playerPunished, playerTeamValue))
					addedPlayers.append(playerName)				
		
		for player in g_jugadores:
			if player not in addedPlayers:
				addedPlayers.append(player)
				dayClassification.append((player, 0, False, 0))
				
		dataToInsert = prepareData(jName, dayClassification)
		insertIntoDatabase(jName, dataToInsert)		
	
def loadResults():
	for root, dirs, files in os.walk(g_resultDir):
		for f in files:
			fullPath = os.path.join(root, f)
			parseResultFile(fullPath, f)
	
def parseArgs(args):
	bOk = False
	strOption = ""
	if (len(args) >= 2):
		if (args[1].lower() == "load"):			
			bOk = True
		elif(args[1].lower() == "list"):
			bOk = True
		elif (args[1].lower() == "day") and (len(args) == 3):
			bOk = True
		elif (args[1].lower() == "alldays"):
			bOk = True
		elif (args[1].lower() == "points"):
			bOk = True
		elif (args[1].lower() == "reset"):
			bOk = True
		elif (args[1].lower() == "history"):
			bOk = True
		elif (args[1].lower() == "delete") and (len(args) == 3):
			bOk = True
		elif (args[1].lower() == "addbolo") and (len(args) == 3):
			bOk = True
		elif (args[1].lower() == "removebolo") and (len(args) == 3):
			bOk = True
		elif (args[1].lower() == "scores"):
			bOk = True	
		elif (args[1].lower() == "player") and (len(args) == 3):
			for player in g_jugadores:
				if(player.lower() == args[2].lower()):
					bOk = True
					break
		elif (args[1].lower() == "winners"):
			bOk = True	
			
	
	if not bOk:
		print("Error. Uso: <py> <option>")
		print("opciones:")
		print("load - Añade a la base de datos los resultados almacenados en el directorio .\\Jornadas ")		
		print("day <idJornada> - Lista los resultados para la jornada indicada ")
		print("list - Lista las jornadas disputadas y cargadas en la BBDD hasta el momento")
		print("alldays - Lista los resultados de todas las jornadas cargadas")
		print("points - Lista los puntos por jornada de cada jugador")
		print("reset - Finaliza la temporada y actualiza los datos")
		print("history - Muestra la clasificacion historica")
		print("delete <idJornada> - Elimina los resultados para la jornada indicada ")
		print("addBolo <userName> - Añade un bolo veraniego como ganado al usario pasado ")
		print("removeBolo <userName> - quita un bolo veraniego como ganado al usario pasado ")
		print("scores - Muestra las 10 mejores y las 10 peores puntuaciones")	
		print("player <nombre> - Muestra Info del jugador")			
	else:
		strOption = args[1]	
		
	return bOk,strOption

def showGlobalClassification():
	loadedDays = getLoadedDaysStr()
	numDays = len(loadedDays)
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute('SELECT * FROM TJugador')
	data = c.fetchall()
	data.sort(key=itemgetter(2,8), reverse = True)
	print("\n\nCLASIFICACION GLOBAL\n\n")
	g_resultsFile.write("CLASIFICACION GLOBAL\n")
	print("Pos\tNombre\tTitulos\tPuntos\tJornadas Ganadas\tMedia\tHistorico\tPasta\tCucharas\tBolos")
	print("---------------------------------------------------------------------------------------------------------------------")
	g_resultsFile.write("Pos;Nombre;Titulos;Puntos;Jornadas Ganadas;Media;Historico;Pasta;Cucharas de Madera;Bolos Veraniegos\n")
	
	pos = 1
	totalMoney = 0
	for playerData in data:
		money = playerData[3]/100
		average = 0
		if(numDays > 0):
			average = playerData[2] / numDays
		strAverage = "%3.2f" % average
		print("{0}\t{1}\t{2}\t{3}\t{4}\t\t\t{5}\t{6}\t\t{7}\t{8}\t\t{9}".format(pos, playerData[1], playerData[4],playerData[2], playerData[8], strAverage, playerData[5], money, playerData[6], playerData[7]))
		g_resultsFile.write("{0};{1};{2};{3};{4};{5};{6};{7};{8};{9}\n".format(pos, playerData[1], playerData[4], playerData[2], playerData[8], strAverage, playerData[5], money, playerData[6], playerData[7]))
		totalMoney = totalMoney + money
		pos = pos + 1		
	
	print("---------------------------------------------------------------------------------------------------------------------")
	print("Pasta Total: {0:.2f}".format(totalMoney))
	g_resultsFile.write("TOTAL;;;;{0:.2f};\n".format(totalMoney))
		
	conn.commit()
	conn.close()
	
def getDBDayData(idJornada):
	'''
	devuelve una lista con los resultados de una jornada determinada
	'''
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute("SELECT TJugador.name, TPuntuacion.puntos, TPuntuacion.pasta, TPuntuacion.jugadorID FROM TJugador,TJornada JOIN TPuntuacion ON TJugador.id = TPuntuacion.jugadorID AND TJornada.id = TPuntuacion.jornadaID AND (TJornada.id =?)", [idJornada])
	data = c.fetchall()
	data.sort(key=itemgetter(1), reverse = True)
	conn.commit()
	conn.close()
	
	return data
	
def printDayData(dayName, idJornada):
	data = getDBDayData(idJornada)
	print(dayName)
	print("Pos\tNombre\tPuntos\tPasta")
	pos = 1
	for reg in data:
		print("{0}\t{1}\t{2}\t{3}".format(pos, reg[0], reg[1], reg[2]/100))
		pos = pos + 1			
		
def printDay(strNumDay):
	dayName = "JORNADA " + strNumDay
	bLoaded, idJornada = isDayPrevioslyLoaded(dayName)
	if bLoaded:	
		printDayData(dayName, idJornada)
	else:
		print("Jornada no cargada: {0}".format(dayName))
		
def deleteDayResults(strNumDay):
	dayName = "JORNADA " + strNumDay
	bLoaded, idJornada = isDayPrevioslyLoaded(dayName)	
	if bLoaded:	
		data = getDBDayData(idJornada)
		conn = sqlite3.connect(g_dataBaseName)
		c = conn.cursor()		
		winner = 1
		for reg in data:
			money = reg[2]
			points = reg[1]
			playerID = reg[3]			
			c.execute("UPDATE TJugador SET puntos = puntos - ?, pasta = pasta - ?, historicoPuntos = historicoPuntos - ?, parciales = parciales - ? WHERE id = ?",[points, money, points, winner, playerID])
			'''solo se resta al primero que es el ganador de la jornada'''
			winner = 0
		'''Se borra La jornada'''		
		c.execute("UPDATE TJornada SET completed = 0 WHERE id = ?",[idJornada])
		c.execute("DELETE FROM TPuntuacion WHERE (TPuntuacion.jornadaID =?)", [idJornada])
		conn.commit()
		conn.close()	
	else:
		print("Jornada no cargada: {0}".format(dayName))
	
def getLoadedDaysStr():
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute('SELECT * FROM TJornada')
	data = c.fetchall()
	loadedDays = []
	for dayData in data:
		if(int(dayData[2]) == 1):
			loadedDays.append([dayData[1], int(dayData[0])])
	
	conn.commit()
	conn.close()
	return loadedDays
	
def listLoadedDays():
	print("\n\nJornadas Disputadas:")
	loadedDays = getLoadedDaysStr()
	for day in loadedDays:
		print(day[0])
	
def listAllDays():
	loadedDays = getLoadedDaysStr()
	for dayData in loadedDays:
		printDayData(dayData[0], dayData[1])		
		
def listPoints():
	pointsPerDay = {}
	strPlayers = ""
	fileStrPlayers = ""
	for player in g_jugadores:
		pointsPerDay[player] =  []		
	loadedDays = getLoadedDaysStr()
	for dayData in loadedDays:
		dbDayData = getDBDayData(dayData[1])
		for reg in dbDayData:
			pointsPerDay.get(reg[0]).append(reg[1])
	
	for key in pointsPerDay:
		strPlayers = strPlayers + "{0}".format(key) + "\t"
		fileStrPlayers = fileStrPlayers + "{0}".format(key) + ";"
		
	print(strPlayers)
	g_resultsFile.write(fileStrPlayers + "\n")
	for i in range (0, len(loadedDays)):		
		strDayPoints = ""
		fileStrDayPoints = ""
		for key in pointsPerDay:
			strDayPoints = strDayPoints + "{0}".format(pointsPerDay.get(key)[i]) + "\t"
			fileStrDayPoints = fileStrDayPoints + "{0}".format(pointsPerDay.get(key)[i]) + ";"
		print(strDayPoints)
		g_resultsFile.write(fileStrDayPoints + " \n")
		
def resetSeason():
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	#quitar el completed de todas las jornadas	
	c.execute("UPDATE TJornada SET completed = 0")
	#eliminar todos los registros de la tabla puntuacion
	c.execute("DELETE FROM TPuntuacion")
	#TJugador Se eliminan los puntos, primas, etc, sólo se respeta el historico
	c.execute('SELECT * FROM TJugador')
	data = c.fetchall()
	data.sort(key=itemgetter(2,8), reverse = True)
	looserPos = len(data) - 1
	winnerPoints = data[0][2]	 
	print("Ganador de la temporada: {0} {1}".format(data[0][1], winnerPoints))
	print("Cuchara de Madera: {0} {1} ".format(data[looserPos][1], data[looserPos][2]))
	c.execute("UPDATE TJugador SET puntos = 0, pasta = 0, parciales = 0")
	c.execute("UPDATE TJugador SET titulos = titulos + 1 WHERE id = ?", [data[0][0]])
	c.execute("UPDATE TJugador SET cucharas = cucharas + 1 WHERE id = ?", [data[looserPos][0]])
	conn.commit()
	conn.close()
	
def manageBolos(userName, addBolo):
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute('SELECT trofeos FROM TJugador WHERE name=?', [userName])
	data = c.fetchall()
	if(1 == len(data)):
		value = data[0][0]
		newValue = False
		if(True == addBolo):
			value = value + 1
			newValue = True	
		elif(value > 0):
			value = value - 1
			newValue = True
					
		if(True == newValue):
			c.execute("UPDATE TJugador SET trofeos = ? WHERE name = ?",[value, userName])
	else:
		print("Jugador {0} no existe".format(userName))
	
	conn.commit()
	conn.close()

def showHistory(playerName):	
	bOnePlayer = False
	if(len(playerName) > 0):
		bOnePlayer = True
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute('SELECT * FROM TJugador')
	data = c.fetchall()
	data.sort(key=itemgetter(4,7,5), reverse = True)
	if(False == bOnePlayer):
		print("\n\nCLASIFICACION HISTORICA\n\n")
	print("Pos\tNombre\tTitulos\thistorico\tCucharas\tBolos Veraniegos")
	
	pos = 1
	for playerData in data:
		if(bOnePlayer and playerData[1].lower() == playerName.lower()) or(False == bOnePlayer):
			print("{0}\t{1}\t{2}\t{3}\t\t{4}\t\t{5}".format(pos, playerData[1], playerData[4], playerData[5], playerData[6], playerData[7]))
		pos = pos + 1		
		
	conn.commit()
	conn.close()
	
def scores():
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute("SELECT TJugador.name, TPuntuacion.puntos, TPuntuacion.jornadaID FROM TJugador JOIN TPuntuacion ON TJugador.id = TPuntuacion.jugadorID")
	data = c.fetchall()
	data.sort(key=itemgetter(1), reverse = True)
	print("\nPUNTUACIONES DESTACADAS\t\t\t\t\tPUNTUACIONES LAMENTABLES\n\n")
	print("Pos\tNombre\tPuntos\tJornada\t\t\t\tNombre\tPuntos\tJornada")
	lastPos = len(data) - 1
	if(len(data) > 0):
		for i in range(0,10):		
			print("{0}\t{1}\t{2}\t{3}\t\t\t\t{4}\t{5}\t{6}".format(i + 1, data[i][0], data[i][1], data[i][2], data[lastPos - i][0], data[lastPos - i][1], data[lastPos - i][2]))		
	conn.commit()
	conn.close()
	
def getPlayerDataByDays(playerName):
	conn = sqlite3.connect(g_dataBaseName)
	c = conn.cursor()
	c.execute("SELECT TJornada.id, TPuntuacion.puntos, TPuntuacion.pasta FROM TJugador,TJornada JOIN TPuntuacion ON TJugador.id = TPuntuacion.jugadorID AND TJornada.id = TPuntuacion.jornadaID AND (TJugador.Name =?)", [playerName])	
	data = c.fetchall()
	data.sort(key=itemgetter(0))
	numJornadas = 0
	totalPuntos = 0
	totalPasta = 0
	partialResults = getPlayerByDayGlobalPosition(playerName)
	print("Num\tJornada\tPuntos\tPasta\tPos\tPos General")
	for reg in data:
		numJornadas = numJornadas + 1
		posJornada = int((reg[2] / g_PunishIncrement) + 1)
		print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(numJornadas, reg[0], reg[1], reg[2] / 100, posJornada, partialResults[numJornadas - 1]))		
		totalPuntos = totalPuntos + reg[1]
		totalPasta = totalPasta + reg[2]
		
	c.execute('SELECT * FROM TJugador')
	data = c.fetchall()
	data.sort(key=itemgetter(2,8), reverse = True)
	currentPos = 0
	for reg in data:
		currentPos = currentPos + 1
		if(reg[1] == playerName):
			break
	
	print("\nTOTAL\n")
	print("Jornadas\tPosicion\tPuntos\tMedia\tPasta")
	print("{0}\t\t{1}º\t\t{2}\t{3:.2f}\t{4}".format(numJornadas,currentPos,totalPuntos,totalPuntos / numJornadas, totalPasta/100))
	conn.commit()
	conn.close()

def getPlayerByDayGlobalPosition(playerName):
	result = []
	partialClassification = {}
	for player in g_jugadores:
		partialClassification[player] = 0
	loadedDays = getLoadedDaysStr()
	for dayData in loadedDays:
		dbDayData = getDBDayData(dayData[1])
		for reg in dbDayData:
			partialClassification[reg[0]] = partialClassification[reg[0]] + reg[1]
		lItems = sorted(partialClassification.items(), key=itemgetter(1), reverse = True)
		pos = 0
		for reg in lItems:
			pos = pos + 1
			if(playerName == reg[0]):
				result.append(pos)
				break
		
	return result
	
def showPlayerInfo(playerName):
	print("Historico\n")
	officialPlayerName = playerName
	for name in g_jugadores:
		if(name.lower() == playerName.lower()):
			officialPlayerName = name
			break;
	showHistory(officialPlayerName)
	print("\nTemporada Actual")
	getPlayerDataByDays(officialPlayerName)	

def showWinners():
	print("Ganadores de Jornadas\n")
	loadedDays = getLoadedDaysStr()
	winners = {}
	for dayData in loadedDays:
		dbDayData = getDBDayData(dayData[1])
		playerName = dbDayData[0][0]
		print("JORNADA {0}\t{1}\t{2}".format(dayData[1], playerName, dbDayData[0][1]))	
		if(playerName not in winners.keys()):
			winners[playerName] = 1
		else:
			winners[playerName] = winners[playerName] + 1
	print("\nTotal")
	print("Jugador\t\tJornadas Ganadas")
	winners = sorted(winners.items(),key=itemgetter(1), reverse = True)
	for winner in winners:
		print("{0}\t\t{1}".format(winner[0], winner[1]))
	
#MAIN
if (not os.path.exists(g_dataBaseName)):	
	createDataBase()
	
bOkParams, strOption = parseArgs(sys.argv)

bOk = False
try:
	g_resultsFile = open(g_resultsFileName, "w")
	bOk = True	
except:
	print("Error inesperado:", sys.exc_info()[0])
	
	
if bOk:
	bShowGlobalData = True
	if bOkParams:
		if ("load" == strOption.lower()):
			loadResults()
		elif ("day" == strOption.lower()):
			printDay(sys.argv[2])
		elif ("list" == strOption.lower()):
			listLoadedDays()
		elif ("alldays" == strOption.lower()):
			listAllDays()
		elif ("points" == strOption.lower()):
			listPoints()
			bShowGlobalData = False
		elif ("reset" == strOption.lower()):
			resetSeason()
		elif ("history" == strOption.lower()):
			emptyStr = ""
			showHistory(emptyStr)
			bShowGlobalData = False
		elif ("delete" == strOption.lower()):
			deleteDayResults(sys.argv[2])		
		elif ("addbolo" == strOption.lower()):
			manageBolos(sys.argv[2], True)		
		elif ("removebolo" == strOption.lower()):
			manageBolos(sys.argv[2], False)
		elif ("scores" == strOption.lower()):
			scores()
			bShowGlobalData = False	
		elif ("player" == strOption.lower()):
			showPlayerInfo(sys.argv[2])	
			bShowGlobalData = False
		elif ("winners" == strOption.lower()):
			showWinners()	
			bShowGlobalData = False			

	if (bShowGlobalData):
	 showGlobalClassification()	

	g_resultsFile.close();




