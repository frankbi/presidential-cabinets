#!/usr/bin/python

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
	#	getData(table)
	getData(tables[2])

def getData(table):

	innerTable = table.find("table", {"class":"navbox-inner"})
	rows = innerTable.findAll("tr", style="")
	extractCabinet(rows[1:])
	obj = {
		"admin": extractPresident(rows[0]),
		"cabinet": extractCabinet(rows[1:])
	}
	# print json.dumps(obj)

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
	return splitYears(arg, 0)

def getEndYear(arg):
	return splitYears(arg, 1)

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