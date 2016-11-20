from bs4 import BeautifulSoup
import urllib
import datetime

def get_restaurants():
	page = urllib.urlopen('https://studentaffairs.duke.edu/forms/dining/menus-hours/').read()
	soup = BeautifulSoup(page, 'html.parser')
	restaurant_data = soup.body.find_all(id='schedule_place_data')
	times = soup.body.find_all(id='schedule_time_data')

	time_data = []
	dates = []
	for t in times:
   		if ':' in t.text or t.text == 'Closed':
   			time_data.append(t)
   		else:
   		if(len(dates) < 5):
			dates.append(t.text[t.text.find("y") + 1:len(t.text)])
	timeIndex = 0
	for restaurant in restaurant_data:
		if(restaurant=='Restaurant'):
			timeIndex = timeIndex + 1
			continue
		for anchor in restaurant.find_all('a'):
			name = anchor.text
			dayOne = time_data[timeIndex]
			tOne= dayOne.split('-')
			datetime = datetime.datetime.strptime("07/27/2012"," %m/%d/%Y")
			isOpen(tOne[0], tTwo[1], requestTime)
			dayTwo = dayOne.next_sibling
			dayThree = dayTwo.next_sibling
			dayFour = dayThree.next_sibling
			dayFive = dayFour.next_sibling
			timeIndex = timeIndex + 5