#!/usr/bin/python

import sys
import os
import glob
import re
from pprint import pprint
import json



# Extracts the usable lines of an access log file
def extract_lines(strRaw):
	strRegex = "(\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(.*?)\]\s\"(\w+)\s(.*?)\s.*?\"\s(\d+)\s\d+"
	objRegex = re.compile(strRegex)
	listRows = re.findall(objRegex, strRaw)
	listOut = []
	for tupSingle in listRows:
		dictTmp = {}
		dictTmp["ip"] = tupSingle[0]
		dictTmp["method"] = tupSingle[2]
		dictTmp["url"] = tupSingle[3]
		dictTmp["status"] = tupSingle[4]
		listOut.append(dictTmp)
	return listOut

def process_file(strFile, dictOutput):
	fh = open(strFile, 'r')
	strRaw = fh.read()
	fh.close()
	listRawLines = extract_lines(strRaw)
	for dictData in listRawLines:
		strMethod = dictData['method']
		strStatus =  dictData['status']
		strUrl =  dictData['url']
		if dictOutput.has_key(strMethod):
			if dictOutput[strMethod].has_key(strStatus):
				if dictOutput[strMethod][strStatus].has_key(strUrl):
					dictUnit = dictOutput[strMethod][strStatus][strUrl]
					dictUnit["total"] += 1
					setIps = set(dictUnit["ips"])
					setIps.add(dictData['ip'])
					dictUnit["ips"] = list(setIps)
				else:
					dictUnit = {}
					dictUnit["total"] = 1
					dictUnit["ips"] = [ dictData['ip']  ]
			else:
				dictUnit = {}
				dictUnit["total"] = 1
				dictUnit["ips"] = [ dictData['ip']  ]
				dictOutput[strMethod][strStatus] = {}
				dictOutput[strMethod][strStatus][strUrl] = dictUnit
		else:
			dictUnit = {}
			dictUnit["total"] = 1
			dictUnit["ips"] = [ dictData['ip']  ]
			dictOutput[strMethod] = {}
			dictOutput[strMethod][strStatus] = {}
			dictOutput[strMethod][strStatus][strUrl] = dictUnit


	return dictOutput


if __name__ == "__main__":
	dictMain = {}
	for strFile in glob.glob("logs/*.log*"):
		process_file(strFile, dictMain)

	pprint(dictMain)

	strOut = json.dumps(dictMain , sort_keys=True, indent=2, separators=(',', ': '))
	fh = open("output.json", 'w')
	fh.write(strOut)
	fh.close()


