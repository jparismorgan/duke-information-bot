from bs4 import BeautifulSoup
import urllib
import datetime


def clean_date(str_date, day):
    ########################
    ####Cleans a date that comes in as a string of these formats:
    ####Closed
    ####10:30am-12:00am
    ####10:00am-2:00pm 5:00pm-9:00pm
    ####Returns datetime start and end times
    ########################

    if str_date == "Closed":
        return "Closed", "Closed"
    date_split = str_date.split('-')
    start = datetime.datetime.strptime(date_split[0] + ' 2016 ' + day, "%I:%M%p %Y %B %d")
    end = datetime.datetime.strptime(date_split[-1] + ' 2016 ' + day, "%I:%M%p %Y %B %d")
    return start, end

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
            what = 0
        if (len(dates) < 5):
            dates.append(t.text[t.text.find("y") + 1:len(t.text)])
    print time_data
    print dates
    print restaurant_data
    timeIndex = 0
    for restaurant in restaurant_data:
        if (restaurant == 'Restaurant'):
            timeIndex = timeIndex + 1
            continue
        for anchor in restaurant.find_all('a'):
            name = anchor.text
            # print name
            dayOne = time_data[timeIndex]
            dayOneStart, dayOneEnd = clean_date(dayOne.text, dates[0])

            dayTwo = dayOne.next_sibling
            dayTwoStart, dayTwoEnd = clean_date(dayOne.text, dates[0])

            dayThree = dayTwo.next_sibling
            dayThreeStart, dayThreeEnd = clean_date(dayOne.text, dates[0])

            dayFour = dayThree.next_sibling
            dayFourStart, dayFourEnd = clean_date(dayOne.text, dates[0])

            dayFive = dayFour.next_sibling
            dayFiveStart, dayFiveEnd = clean_date(dayOne.text, dates[0])
            timeIndex = timeIndex + 5


if __name__ == '__main__':
    get_restaurants()