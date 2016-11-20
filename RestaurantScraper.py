from bs4 import BeautifulSoup
import urllib

def get_restaurants():
	page = urllib.urlopen('https://studentaffairs.duke.edu/forms/dining/menus-hours/').read()
	soup = BeautifulSoup(page, 'html.parser')
	restaurant_data = soup.body.find_all(id='schedule_place_data')
	times = soup.body.find_all(id='schedule_time_data')

	time_data = []
	print(times)
	dates = []
	for t in times:
   		if ':' in t.text or t.text == 'Closed':
   			time_data.append(t)
   		else:
   		if(len(dates) < 5):
			dates.append(t.text[t.text.find("y") + 1:len(t.text)])
	print(dates)
	timeIndex = 0
	print time_data
	for restaurant in restaurant_data:
		if(restaurant=='Restaurant'):
			timeIndex = timeIndex + 1
			continue
		for anchor in restaurant.find_all('a'):
			first = time_data[timeIndex]
			print("{} {}").format(anchor.text, first.text)
			second = first.next_sibling
			print("{} {}").format(anchor.text, second.text)
			third = second.next_sibling
			print("{} {}").format(anchor.text, third.text)
			fourth = third.next_sibling
			print("{} {}").format(anchor.text, fourth.text)
			fifth = fourth.next_sibling
			print("{} {}").format(anchor.text, fifth.text)
			timeIndex = timeIndex + 5