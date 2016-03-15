import os
import sys

#MAIN
if (len(sys.argv) == 2):
	print(sys.argv[1])
	file = open(sys.argv[1],"rb")
	buffer = file.read()
	print(buffer)
	file.close()
else:
	print("Error. Introducir el path del fichero a abrir");