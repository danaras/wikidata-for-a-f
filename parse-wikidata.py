from urllib2 import Request, urlopen, URLError
import os, json, csv
title =''
language =''
qid=''
entitiesFound = False
output = open('output.csv', 'w')
csvWriter = csv.writer(output)
csvWriter.writerow(['language','title','p21','gender','p106','occupation'])
with open('test.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		info = list(row)
		langTitle = info[0]
		language = langTitle.split(':')[0]
		titleOriginal = langTitle.split(':')[1]
		title = titleOriginal.replace(' ', '+')
		print language
		print title


		request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+language+'wiki&titles='+title+'&languages='+language+'&props=claims%7Clabels&format=json')
		try:
			response = urlopen(request)
			wikiData = response.read()
			jsonData = json.loads(wikiData)
			try:
				keys = jsonData["entities"].keys()
				entitiesFound = True
			except:
				print "cannot find entities"
				entitiesFound = False
			for key in keys:
				qid = key
			print qid
			try:
				p21 = (jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
				print jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
			except:
				print "no p21"
			try:
				p106 = (jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"])
				print jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"]
			except:
				print "no p106"
			if p21:
				pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+p21+'&props=descriptions%7Clabels&languages=en%7Cde%7Cfr&format=json')
				try:
					pResponse = urlopen(pRequest)
					pData = pResponse.read()
					pJsonData = json.loads(pData)
					# print pJsonData
					# print pJsonData["entities"][x]["labels"]["en"]["value"]
					gender = pJsonData["entities"][p21]["labels"]["en"]["value"]

					print gender
				except URLError, e:
				    print 'No kittez. Got an error code:', e
			if p106:
				pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+p106+'&props=descriptions%7Clabels&languages=en%7Cde%7Cfr&format=json')
				try:
					pResponse = urlopen(pRequest)
					pData = pResponse.read()
					pJsonData = json.loads(pData)
					# print pJsonData
					# print pJsonData["entities"][x]["labels"]["en"]["value"]
					occupation = pJsonData["entities"][p106]["labels"]["en"]["value"]

					print occupation
				except URLError, e:
					print 'No kittez. Got an error code:', e
			csvWriter.writerow([language, titleOriginal, p21, gender, p106, occupation])
			p21 = ''
			p106 = ''
			language = ''
			titleOriginal = ''
			gender = ''
			occupation = ''
		except URLError, e:
		    print 'General error. Got an error code:', e
