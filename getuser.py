import getpass
import win32api
import win32con


def printUserName(flag,flagName):
	userName = None
	try:
		userName = win32api.GetUserNameEx (flag)
		print("{0}:{1}\n".format(flagName,userName))
	except:
		print("No existe userName para flag {0}".format(flagName))
		
	


print("getpass.getuser {0}:".format(getpass.getuser()))
print("win32api.GetUserName: {0}".format(win32api.GetUserName()))
printUserName(win32con.NameUnknown, "NameUnknown")
printUserName(win32con.NameFullyQualifiedDN,"NameFullyQualifiedDN")
printUserName(win32con.NameSamCompatible,"NameSamCompatible")
printUserName(win32con.NameDisplay,"NameDisplay")
printUserName(win32con.NameUniqueId,"NameUniqueId")
printUserName(win32con.NameCanonical,"NameCanonical")
printUserName(win32con.NameUserPrincipal,"NameUserPrincipal")
printUserName(win32con.NameCanonicalEx,"NameCanonicalEx")
printUserName(win32con.NameServicePrincipal,"NameServicePrincipal")
printUserName(win32con.NameDnsDomain,"NameDnsDomain")
'''
NameUnknown           = 0,
  NameFullyQualifiedDN  = 1,
  NameSamCompatible     = 2,
  NameDisplay           = 3,
  NameUniqueId          = 6,
  NameCanonical         = 7,
  NameUserPrincipal     = 8,
  NameCanonicalEx       = 9,
  NameServicePrincipal  = 10,
  NameDnsDomain         = 12
'''