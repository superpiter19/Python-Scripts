import types
import win32com
import msvcrt as keys
from datetime import datetime
from struct import *
import threading
import win32com.client
import win32com.server.util
import threading
import pythoncom

EPOCH_AS_FILETIME = 116444736000000000
HUNDREDS_OF_NANOSECONDS = 10000000
waitForFinishEvent = threading.Event()

NOTIFICATION_TUNEUP_PARTIAL_RESULT = 0x04024013
NOTIFICATION_TUNEUP_FINAL_RESULT = 0x04024018                          

win32com.client.gencache.EnsureModule('{5F0CD35D-1A12-4057-97D2-8AE85B376081}', 0, 1, 0) # NdkApi.tlb
win32com.client.gencache.EnsureModule('{14B0921F-969A-4A5D-B8A3-5CBF22E5FE0B}', 0, 1, 0) # NdkCoreApi.tlb
#win32com.client.gencache.EnsureModule('{038F2385-BDAB-4C49-9CC3-B60C51A211E6}', 0, 1, 0) # NdkApiDefs.tlb

######################################################################################
# ndk2String
######################################################################################
def ndk2String(indent, data):
	strResult = ""
	if (indent==None):
		indent = " "
	if not type(data) is types.InstanceType:
		print("1")
		strResult = strResult + "%s%s" % (indent, data) + "\n"
	else:
		for element in data:
			value = None
			if not type(element) is types.InstanceType:
				strResult = strResult + "%s%s" % (indent, element) + "\n"
			else:
				if (element.__class__.__name__=='INDKPair'):
					pair = element
					value = pair.Second
					if type(value) is types.InstanceType:
						strResult = strResult + "%s%s = " % (indent, pair.First) + "\n"						
					else:
						strResult = strResult + "%s%s = %s" % (indent, pair.First, pair.Second) + "\n"							
				else:
					value = element

				if type(value) is types.InstanceType:
					collection = value
					strResult = strResult + " %s{" % (indent) + "\n"
					strResult = strResult + ndk2String(indent + "  ", collection)
					strResult = strResult + " %s}" % (indent) + "\n"
	return strResult
######################################################################################

######################################################################################
def printLastCleanTime(cfg):
	dateHigh = cfg.Get(0,0x4025002)
	dateLow = cfg.Get(0,0x4025003)
	
	if ( (dateHigh > 0) or (dateLow > 0)):
		ft_dec = unpack('>Q', pack('>LL', dateHigh, dateLow))[0]
		dt = datetime.fromtimestamp((ft_dec - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)
		print("Fecha de ultima limpieza: {0}".format(dt))
	
######################################################################################
# class MyCommandListener
class MyListenerAnalysis:
        _com_interfaces_ = ['INDKListener']
        _typelib_guid_ = '{14B0921F-969A-4A5D-B8A3-5CBF22E5FE0B}'
        _typelib_version_ = 1, 0
 
        def Notify(self,ndkEvent):
			global waitForFinishEvent
			e = win32com.client.Dispatch(ndkEvent)
			eventData = e.GetEventData()
			bFinal = False
			for element in eventData:
				if (element.__class__.__name__=='INDKPair'):
					if (element.First == "EventID"):
						if (element.Second == NOTIFICATION_TUNEUP_PARTIAL_RESULT):
							print("PARTIAL_RESULT")
						elif (element.Second == NOTIFICATION_TUNEUP_FINAL_RESULT):
							print("FINAL")
							bFinal = True
						break
			print("*********************************")						
			print(ndk2String(" ", eventData))
			print("*********************************")
			if bFinal:
				waitForFinishEvent.set()



#MAIN


#print("atacheate y pulsa una tecla")
#keys.getch()
systrayAppCtx = win32com.client.Dispatch("NdkApi.NDKApplicationContext")
systrayAppCtx.Initialize("appconfigTest.xml")

# Create 'Ndk.license'
modTuneUp = systrayAppCtx.Get("Ndk.TuneUp")
lAreas = []

print(ndk2String(" ", modTuneUp.GetTuneUpAreas()))

print("TuneUp Status")
print(ndk2String(" ", modTuneUp.GetStatus()))

print("Procesos lanzados:")
print(ndk2String(" ", modTuneUp.GetRunningProcesses()))

bExistsArea = False;
area = 1

print("Areas disponibles")
print("\t1 Windows Temp")
print("\t2 Windows Recycler Bin")
print("\t3 Windows Logs")
print("\t4 Internet Explorer Cookies")
print("\t5 Internet Explorer History")
print("\t6 Internet Explorer Temp")
print("\t7 Chrome Cache")
print("\t8 Chrome Cookies")
print("\t9 Chrome History")
print("\t10 Firefox Cache")
print("\t11 Firefox Cookies")
print("\t12 Firefox History")



notifList = systrayAppCtx.Get("Ndk.List")
strAreas = raw_input("\nIntroduce areas (Separadas por ,)");
tAreas = strAreas.split(",")

for strArea in tAreas:
	area = int(strArea)
	if ((area > 0) and (area < 14)):
		notifList.Add(area)

listenerAnalysis = win32com.server.util.wrap(MyListenerAnalysis())
print("*******************************************************************************")
print("ANALISIS")
print("*******************************************************************************")
modTuneUp.InspectAreas(notifList,listenerAnalysis)

# wait for completion the async command
while (not waitForFinishEvent.isSet()):
		pythoncom.PumpWaitingMessages()
		waitForFinishEvent.wait(0.2)
		
print("*******************************************************************************")
print("FIN ANALISIS")
print("*******************************************************************************")
print("*******************************************************************************")

bActResponse = False

print("Actuar (S-N)")
while not bActResponse:
	strActResponse = keys.getch();
	if (strActResponse == 's' or strActResponse == 'S'):
		bActResponse = True
		waitForFinishEvent = threading.Event()
		listenerAct = win32com.server.util.wrap(MyListenerAnalysis())
		print("*******************************************************************************")
		print("ACTUACION")
		print("*******************************************************************************")
		modTuneUp.ActOnAreas(notifList,listenerAct)
		# wait for completion the async command
		while (not waitForFinishEvent.isSet()):
			pythoncom.PumpWaitingMessages()
			waitForFinishEvent.wait(0.2)
		print("*******************************************************************************")
		print("FIN ACTUACION")
		print("*******************************************************************************")		
	elif (strActResponse == 'n' or strActResponse == 'N'):
		bActResponse = True

