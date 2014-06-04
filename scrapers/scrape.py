#!/usr/bin/python

'''
LAST UPDATED: June 4, 2014
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

	#for table in tables:
	#	print type(json.dumps(getData(table)))
	data = []
	for table in tables:
		data.append(getData(table))
	print json.dumps(data)

	#print getData(tables[0])

def getData(table):
	innerTable = table.find("table", {"class":"navbox-inner"})
	rows = innerTable.findAll("tr", style="")
	extractCabinet(rows[1:])
	# tableList = []
	obj = {
		"admin": extractPresident(rows[0]),
		"cabinet": extractCabinet(rows[1:])
	}
	# tableList.append(obj)
	# return json.dumps(obj)
	return obj

def extractPresident(row):
	innerDiv = row.find("div", style="font-size:110%;")
	years = innerDiv.text[-11:].strip("()")
	anchors = innerDiv.findAll("a")
	return {
		"name": anchors[-1]["title"],
		"url": anchors[-1]["href"],
		"start": years[:4],
		"end": years[5:]
	}

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

def getStartYear(arg):
	s = arg.text
	startYear = s[s.find("(")+1:s.find(")")][:4]
	return startYear

def getEndYear(arg):
	s = arg.text
	startYear = s[s.find("(")+1:s.find(")")][:4]
	endYear = s[s.find("(")+1:s.find(")")][5:]
	if len(endYear) is not 4:
		if endYear == "present":
			return "present"
		if endYear is None:
			return startYear
	else:
		return endYear

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
					"start": getStartYear(member),
					"end": getEndYear(member)
				}
				fullCabinet.append(data)
	return fullCabinet

if __name__ == "__main__":
	init()