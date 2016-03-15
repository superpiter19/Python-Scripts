from win32com.shell import shell, shellcon
import os

print ("Directorio de Cookies de IE:")
print ("\t {0}".format(shell.SHGetFolderPath(0, shellcon.CSIDL_COOKIES, None, 0)))
dirAppData = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)
dirAppLocalData = shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, None, 0)
dirCookiesMozilla = dirAppData + "\\Mozilla\\Firefox\\Profiles"
if (os.path.exists(dirCookiesMozilla)):
	print("Directorio de Cookies de Firefox:")
	print("\t {0}".format(dirCookiesMozilla))
else:
	print("No Tienes Firefox instalado")
dirCookiesChrome = dirAppLocalData + "\\Google\\Chrome\\User Data\\Default"
if (os.path.exists(dirCookiesChrome)):
	print("Directorio de Cookies de Chrome:")
	print("\t {0}".format(dirCookiesChrome))
else:
	print("No Tienes Chrome instalado")
dirCookiesOpera = dirAppData + "\\Opera\\Opera"
if (os.path.exists(dirCookiesOpera)):
	print("Directorio de Cookies de Opera:")
	print("\t {0}".format(dirCookiesOpera))
else:
	print("No Tienes Opera instalado")
dirCookiesSafari = dirAppData + "\\Apple Computer\\Safari\\Cookies"
if (os.path.exists(dirCookiesSafari)):
	print("Directorio de Cookies de Safari:")
	print("\t {0}".format(dirCookiesSafari))
else:
	print("No Tienes Safari instalado")

print(os.path.expandvars("%windir%\\temp"))
print(os.path.expandvars("%USERPROFILE%\\Local Settings\\Temp"))
print(os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Cookies"))
print(os.path.expandvars("%LOCALAPPDATA%\\Microsoft\\Internet Explorer\\DOMStore"))
print("CSIDL_INTERNET_CACHE: {0}".format(shell.SHGetFolderPath(0, shellcon.CSIDL_INTERNET_CACHE, None, 0)))