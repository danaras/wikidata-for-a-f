import os, csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
occupations = []
foundOccupations = []
outputTXT = open('output-occupation-percentages.txt', 'w')
outputCSV = open('output-found-occupations.csv', 'w')
csvWriter = csv.writer(outputCSV)
csvWriter.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
with open('Occupations-VisualArtist.txt', 'r') as f:
	for line in f:
		occupations.append(line.strip())
print occupations
with open('needs-occupation.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		info = list(row)
		firstSentence = info[7]
		print firstSentence
		outputTXT.write("----------------------------------------\n"+firstSentence+"\n")
		for x in occupations:
			what = fuzz.partial_ratio(x, firstSentence)
			print x + ": " + str(what)
			outputTXT.write(x + ": " + str(what)+"\n")
			if what is 100:
				info[6] = x
				csvWriter.writerow(info)
