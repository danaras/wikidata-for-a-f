from urllib2 import Request, urlopen, URLError
import os, json, csv
title =''
language =''
qid=''
p21and106 = []
with open('test.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		info = list(row)
		langTitle = info[0]
		language = langTitle.split(':')[0]
		title = langTitle.split(':')[1]
		title = title.replace(' ', '+')
		print language
		print title


		request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+language+'wiki&titles='+title+'&languages='+language+'&props=claims%7Clabels&format=json')
		try:
			response = urlopen(request)
			wikiData = response.read()
			jsonData=json.loads(wikiData)
			keys = jsonData["entities"].keys()
			for key in keys:
				qid = key
			print qid
			p21and106.append(jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
			p21and106.append(jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"])
			print jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
			print jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"]
			for x in p21and106:
				pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+x+'&props=descriptions%7Clabels&languages=en%7Cde%7Cfr&format=json')
				try:
					pResponse = urlopen(pRequest)
					pData = pResponse.read()
					pJsonData = json.loads(pData)
					# print pJsonData
					# print pJsonData["entities"][x]["labels"]["en"]["value"]
					gender = pJsonData["entities"][x]["labels"]["en"]["value"]

				except URLError, e:
				    print 'No kittez. Got an error code:', e
			p21and106 = []
		except URLError, e:
		    print 'No kittez. Got an error code:', e
