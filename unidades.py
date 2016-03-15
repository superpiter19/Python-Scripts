import sys
import os
import glob

KB = 1024
MB = KB * KB
GB = MB * KB

if (len(sys.argv) != 2):
	print("Uso <py> <numero que quieras transformar>")
else:
	number = int(sys.argv[1])
	if (number > GB):
		print("{0} GBs".format(number/GB))
	elif (number > MB):
		print("{0} MBs".format(number/MB))
	elif (number > KB):
		print("{0} KBs".format(number/KB))
	else:
		print("{0} Bytes".format(number))
		