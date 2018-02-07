import os, csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
occupations = []
foundOccupations = []
output = open('output-occupation-percentages.txt', 'w')
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
		output.write("----------------------------------------\n"+firstSentence+"\n")
		for x in occupations:
			what = fuzz.partial_ratio(x, firstSentence)
			print x + ": " + str(what)
			output.write(x + ": " + str(what)+"\n")
