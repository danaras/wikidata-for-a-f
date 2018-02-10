import os, csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
firstline = True
linkList = []
ignoreList = ['facebook', 'moma', 'wikipedia', 'wikimedia']
firstLastName = ''
outputCSV = open('output-references.csv', 'w')
csvWriter = csv.writer(outputCSV)
csvWriter.writerow(['firstLastName','QID','property id','property value','occupationQID','stated in','ref link', 'context'])
def scrape_inside_link(br, link, keyword):
	br.get(link)
	try:
		WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH,"//*[contains(text(), '"+occupation+"')]")))
	except TimeoutException:
		print("timed out waiting for the reference to load")
	context = br.find_elements_by_xpath("//*[contains(text() , '"+occupation+"')]")
	for x in context:
		print x.text
		csvWriter.writerow([firstLastName, qid, propertyId, occupation, occupationQID, statedIn, link, x.text])
def scrape_result_links(br):
	# Xpath will find a subnode of h3, a[@href] specifies that we only want <a> nodes with
	# any href attribute that are subnodes of <h3> tags that have a class of 'r'
	links = browser.find_elements_by_xpath("//h3[@class='r']/a[@href]")
	results = []
	for link in links:
		title = link.text.encode('utf8')
		url = link.get_attribute('href')
		if not any(word in url.lower() for word in ignoreList):
			title_url = (title, url)
			results.append(title_url)
	return results
with open('output-found-occupations.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		if firstline:    #skip first line
			firstline = False
			continue
		info = list(row)
		firstLastName = unicode(info[1], errors = 'ignore')
		occupation = unicode(info[6], errors = 'ignore')
		qid = unicode(info[2], errors = 'ignore')
		propertyId = "P106"
		occupationQID = unicode(info[5], errors = 'ignore')
		statedIn = "P248"
		browser = webdriver.Chrome(executable_path='//Library/Application Support/Google/chromedriver')
		browser.get('https://www.google.com/')

		timeout = 10
		try:
			WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="hplogo"]/canvas')))
		except TimeoutException:
			print("timed out waiting for the google page to load")
			browser.quit()
		search = browser.find_element_by_name('q')
		search.send_keys(firstLastName + ' ' + occupation)
		search.submit()
		try:
			WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="nav"]/tbody/tr')))
		except TimeoutException:
			print("timed out waiting for the google search results page to load")
			# browser.quit()
		all_results = []
		titles_urls = scrape_result_links(browser)
		for title in titles_urls:
			all_results.append(title)

		for result in all_results[:5]:
			title = result[0]
			url = result[1]
			print firstLastName + ' ----- ' + occupation
			print '[+]', title, '--', url
			scrape_inside_link(browser, url, occupation)
		firstLastName = ''

		browser.quit()
