import win32api
import os

path = "c:\\Documents and Settings\\pcantero\\MYDOCU~1\\session01.rar"
print(path)
print(win32api.GetLongPathName(path))
