#!/usr/bin/python

'''
LAST UPDATED: June 5, 2014
BY: Frank Bi
EMAIL: fbi@newshour.org
'''

from bs4 import BeautifulSoup
import simplejson as json
import requests
import re

def init():
	url = "http://en.wikipedia.org/wiki/List_of_United_States_Cabinets"
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	body = soup.find("div", {"id":"mw-content-text"})
	tables = soup.findAll("table", {"class":"navbox"})
	data = []
	for table in tables:
		data.append(getData(table))
	print json.dumps(data, indent=2)

def getData(table):
	innerTable = table.find("table", {"class":"navbox-inner"})
	rows = innerTable.findAll("tr", style="")
	tables = innerTable.findAll("table")
	president = extractPresident(rows[0])
	if len(tables) is 0:
		obj = {
			"admin": president,
			"cabinet": extractCabinet(rows[1:])
		}
		return obj
	elif len(tables) is 2:
		rows = tables[0].findAll("tr", style="")
		obj = {
			"admin": president,
			"cabinet": extractCabinet(rows[1:])
		}
		return obj

def extractPresident(row):
	innerDiv = row.find("div", style="font-size:110%;")
	headerText = innerDiv.text
	anchors = innerDiv.findAll("a")
	return {
		"name": anchors[-1]["title"],
		"url": anchors[-1]["href"],
		"start": getPrezYears(headerText, 0),
		"end": getPrezYears(headerText, 1)
	}

def getPrezYears(text, which):
	startIndex = text.index("(")
	endIndex = text.index(")")
	years = text[startIndex+1:endIndex]
	digitsOnly = re.compile("\D")
	if bool(digitsOnly.search(years)):
		if len(years) is 9:
			if which is 0:
				return years[:4]
			if which is 1:
				return years[5:]
		else:
			if bool(re.match("since", years)):
				if which is 0:
					return re.sub("[^0-9]", "", years)
				else:
					return "Current"
	elif len(years) is 4:
		return years

def splitYears(arg, which):
	arg = arg.text.strip(" ()")
	if len(arg) is 4:
		return arg
	else:
		if which is 0:
			if len(arg) is 9:
				return arg[:4]
		if which is 1:
			if len(arg) is 9:
				return arg[5:]

def getStartEndYears(arg, which):
	string = arg.text
	try:
		startIndex = string.index("(")
		endIndex = string.index(")")
	except Exception:
		return "ERR"
	years = string[startIndex+1:endIndex]
	if len(years) is 4:
		if which is 0:
			return years
		elif which is 1:
			return years
	elif len(years) is 9:
		if which is 0:
			return years[:4]
		elif which is 1:
			return years[5:]
	elif bool(re.search("present", years)):
		if which is 0:
			return years[:4]
		if which is 1:
			return "Current"
	else:
		return "ERR"


def extractCabinet(rows):
	fullCabinet = []
	for row in rows:
		cabinetMembers = row.findAll("li")
		for member in cabinetMembers:
			anchor = member.find("a")
			if anchor is not None:
				data = {
					"name": re.sub(r"\([^)]*\)", "", anchor["title"]).strip(),
					"position": row.find("th", {"scope":"row"}).text,
					"url": anchor["href"],
					"start": getStartEndYears(member, 0),
					"end": getStartEndYears(member, 1),
					"personal": getPersonal(anchor["href"])
				}
				fullCabinet.append(data)
	return fullCabinet

def getPersonal(url):
	baseUrl = "http://en.wikipedia.org"
	fullUrl = baseUrl + url
	r = requests.get(fullUrl)
	soup = BeautifulSoup(r.text)
	return {
		"photo": getPhoto(soup),
		"bday": getBDay(soup),
		"dday": getDDay(soup)
	}

def getBDay(obj):
	bday = obj.findAll("span", {"class","bday"})
	if len(bday) is 1:
		return bday[0].text
	else:
		return "ERR"

def getDDay(obj):
	dday = obj.findAll("span", {"class","dday"})
	if len(dday) is 1:
		return dday[0].text
	else:
		return "ERR"

def getPhoto(obj):
	infoBox = obj.findAll("table", {"class","vcard"})
	if len(infoBox) is 1:
		imageList = infoBox[0].findAll("a", {"class","image"})
		if bool(imageList):
			return "http:" + imageList[0].find("img")["src"]
		else:
			return "ERR"

if __name__ == "__main__":
	init()