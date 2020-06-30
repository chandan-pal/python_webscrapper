
# Enter your search string here
STR_TO_FIND = 'search string here'

# Enter the URL here
URL = 'https://chandan-pal.github.io'

# Authentication (basic)
user = '*********'
pwd = '*********'

import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Make a request to the base url : here also turning of SSL verification for my specific need
page = requests.get(URL, auth=HTTPBasicAuth(user, pwd), verify=False)

# parse the response as html
soup = BeautifulSoup(page.content, 'html.parser')

# from response find all the td elements with class=link
instances = soup.find_all('td', class_='link')

# for each link find the url of the link from href property
for i in instances:
	link = i.find('a')['href']
	
	fileFound = False
	if link != '../':
		# make a new request to each link
		mbombopPage = requests.get(URL+'/'+link+'mbombop'+'/', auth=HTTPBasicAuth(user, pwd), verify=False)
		
		# parse the response as html
		s = BeautifulSoup(mbombopPage.content, 'html.parser')
		
		# find all the log file links the page
		logTd = s.find_all('td', class_='link')
		
		# for each log file make a response to the log file and get the contents of log file as response
		for j in logTd:
			logfilelink =j.find('a')['href']
			if logfilelink != '../':
				log_file_url = URL+'/'+link+'mbombop'+'/'+logfilelink
				filedata = requests.get(log_file_url, auth=HTTPBasicAuth(user, pwd), verify=False)
				
				# find the serch string in the response, if found, break both loops
				if str(filedata.content).find(STR_TO_FIND) >= 0:
					fileFound = True
					print('LOG_FILE=', log_file_url)
					break
		if fileFound:
			break
