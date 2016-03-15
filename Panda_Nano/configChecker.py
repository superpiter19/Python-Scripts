# -*- coding: utf-8 -*-

import sys
import argparse
import win32com.client

##############################################################################################################################
# Initialization
##############################################################################################################################

# vars
dbItemsCollection = {}

# NDK
appCtx = None
ctx = None
cfg = None
xmldbXmlDoc = None

nullValue = "null"
errorValue = "ERROR!"
typeUnknownString = "UNKNOWN TYPE!"

##############################################################################################################################
# XML Utils
##############################################################################################################################

# parse_xmldb node
def parse_node(node, itemsCollection):
	if node.childNodes.length!=0:
		if (node.nodeName=="Item"):
			parse_Item(node, itemsCollection)
		else:
			for child in node.childNodes:
				parse_node(child, itemsCollection)
		
# parse_xmldb node
def parse_Item(node, itemsCollection):
	itemData = {}
	itemData["id"] = node.getAttribute("Id")
	itemData["name"] = node.getAttribute("Name")
	itemData["type"] = node.getAttribute("Type")
	itemData["comment"] = node.getAttribute("Comment")

	if (itemData["comment"]==None):
		itemData["comment"] = node.text
	getItemValue(node, itemData)
		
	if (args.gets_config or args.check_config):
		if (args.gets_config):
			itemData["value"] = get_ndkItem(parseInt(itemData["id"]))
		else:
			itemData["currentValue"] = get_ndkItem(parseInt(itemData["id"]))
		node.SetAttribute("Comment", itemData["comment"])
		setItemValue(node, itemData)

	itemsCollection[itemData["id"]] = itemData

# getItemValue
def getItemValue(node, itemData):
	valueNode = node.selectSingleNode("Value")
	if (valueNode!=None):
		type = itemData["type"]
		value = valueNode.getAttribute("Value")
		if (value==errorValue):	itemData["value"] = value
		elif (type=="STRING"):	itemData["value"] = value
		elif (type=="DWORD"): 	itemData["value"] = parseInt(value)
		elif (type=="BOOL"):
			if (value=="true"): itemData["value"] = True
			else: itemData["value"] = False
		elif (type=="CSimpleSerializableList<STRING>"):
			value_list = []
			list = valueNode.selectSingleNode("List")
			if (list!=None):
				listChild = list.firstChild
				while (listChild!=None):
					value_list.append(listChild.getAttribute("Value"))
					listChild = listChild.nextSibling
			itemData["value"] = value_list
		elif (type=="CSimpleSerializableList<DWORD>"):
			value_list = []
			list = valueNode.selectSingleNode("List")
			if (list!=None):
				listChild = list.firstChild
				while (listChild!=None):
					value_list.append(parseInt(listChild.getAttribute("Value")))
					listChild = listChild.nextSibling
			itemData["value"] = value_list
		else:
			itemData["value"] = typeUnknownString
	else:
		itemData["value"] = ""

# setItemValue
def setItemValue(node, itemData):
	type = itemData["type"]
	value = itemData["value"]
	currentValue = None
	if (args.check_config):
		currentValue = itemData["currentValue"]
		
	node.text = ""
	newValue = xmldbXmlDoc.createElement("Value")
	if (type=="STRING"):	setValueNodeAttribute(newValue, value, currentValue)
	elif (type=="DWORD"): 	setValueNodeAttribute(newValue, DWORD2String(value), DWORD2String(currentValue))
	elif (type=="BOOL"):	setValueNodeAttribute(newValue, BOOL2String(value), BOOL2String(currentValue))
	elif (type=="CSimpleSerializableList<STRING>"):
		listNode = xmldbXmlDoc.createElement("List")
		it = 0
		if (value==errorValue): count = 0
		else:					count = len(value)
		if ((currentValue!=None) and (len(currentValue) > count)): count = len(currentValue)
		for it in range(count):
			itValue = None
			if (value==errorValue): itValue = errorValue
			elif (it<len(value)):
				itValue = value[it]
			itCurrentValue = None
			if ((currentValue!=None) and (it<len(currentValue))):
				itCurrentValue = currentValue[it]
			elementNode = xmldbXmlDoc.createElement("Element")
			setValueNodeAttribute(elementNode, itValue, itCurrentValue)
			listNode.appendChild(elementNode)
			it = it + 1
		newValue.appendChild(listNode)
	elif (type=="CSimpleSerializableList<DWORD>"):
		listNode = xmldbXmlDoc.createElement("List")
		it = 0
		if (value==errorValue): count = 0
		else:					count = len(value)
		if ((currentValue!=None) and (len(currentValue) > count)): count = len(currentValue)
		for it in range(count):
			itValue = None
			if (value==errorValue): itValue = errorValue
			elif (it<len(value)):
				itValue = value[it]
			itCurrentValue = None
			if ((currentValue!=None) and (it<len(currentValue))):
				itCurrentValue = currentValue[it]
			elementNode = xmldbXmlDoc.createElement("Element")
			setValueNodeAttribute(elementNode, DWORD2String(itValue), DWORD2String(itCurrentValue))
			listNode.appendChild(elementNode)
			it = it + 1
		newValue.appendChild(listNode)
	else:
		setValueNodeAttribute(newValue, typeUnknownString, typeUnknownString)
	node.appendChild(newValue)
	
# setNodeAttribute
def setValueNodeAttribute(node, textValue, textCurrentValue):
	if (textValue!=None): 
		node.SetAttribute("Value", textValue)
	elif (textCurrentValue!=None): 
		node.SetAttribute("Value", nullValue)
			
	if (textCurrentValue!=None):
		if ((textValue==None) or (textValue!=textCurrentValue)): 
			node.SetAttribute("currentValue", textCurrentValue)
	elif ((textValue!=None) and (args.check_config)): 
		node.SetAttribute("currentValue", nullValue)

# DWORD2String
def DWORD2String(value):
	if ((value==None) or (value==errorValue)): return value
	else: 
		try: return hex(long(value))
		except: return errorValue

# BOOL2String
def BOOL2String(value):
	if ((value == None) or (value == errorValue)): return value
	else: 
		if (value): return "true"
		else: return "false"
	
# parseInt
def parseInt(text):
	try:
		return long(text,0)
	except:
		return 0
	
##############################################################################################################################
# NDK Utils
##############################################################################################################################
def ndkInit():
	global appCtx, ctx, cfg
	appCtx = win32com.client.Dispatch("NdkApi.NDKApplicationContext")
	ctx = appCtx.Create("Ndk.Context", None)
	ctx.Insert("ContextCommunication", appCtx.Create("Ndk.Communication", ctx))
	cfg = appCtx.Create("Ndk.Configuration", ctx)

def get_ndkItem(itemId):
	try:
		return cfg.Get(parseInt(args.profile), itemId)
	except:
		return errorValue
	
#############################################################################################################################
# main
#############################################################################################################################
parser = argparse.ArgumentParser(description='NDK configuration checker')
parser.add_argument('-g', '--gets_config', action='store_true', help='Gets the configuration from the installed PRODUCT')
parser.add_argument('-c', '--check_config', action='store_true', help='Checks the configuration into the installed PRODUCT')
parser.add_argument('-xmldb', '--xmldb', required=True, help='XML configuration items db.')
parser.add_argument('-profile', '--profile', default="0", help='Configuration profile.')
args = parser.parse_args()

if (len(sys.argv)==3):
	print 
	print 
	print parser.print_help() 
	sys.exit()

if (not (args.gets_config ^ args.check_config)):
	print 
	print 
	print "ERROR: Cannot specify -g and -c together in same commandline."
	print 
	print parser.print_help()
	sys.exit()
	
print 
print 
print "Using config profile: " + args.profile
print 
	
#init NDK
ndkInit()
	
# Parse xmldb
if (args.xmldb!=None):
	xmldbXmlDoc = win32com.client.Dispatch("Msxml2.DOMDocument")
	xmldbXmlDoc.Async = False
	xmldbXmlDoc.load(args.xmldb)
	parse_node(xmldbXmlDoc.documentElement, dbItemsCollection)

# Gets config
if (args.check_config):
	xmldbXmlDoc.Save(args.xmldb + ".check_result.xml")
elif (args.gets_config):
	xmldbXmlDoc.Save(args.xmldb + ".gets_result.xml")
