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

restaurants = {"Au Bon Pain": ["bakery","sandwich","salad","soup", "vegetarian"],
			   "Bella Union": ["coffee,candy,pastries"],
			   "Blue Express": ["mediterranean", "sandwich", "salad", "dessert", "vegetarian"],
			   "Cafe": ["crepe", "panini", "gelato", "smoothies", "juice", "coffee"],
			   "Cafe at Smith Warehouse": ["sandwich", "salad", "dessert"],
			   "Cafe De Novo": ["sandwich", "salad", "dessert"],
			   "Cafe Edens": ["sandwich", "salad", "dessert"],
			   "Dame's Express": ["sandwich", "salad", "dessert", "chicken", "waffles"],
			   "Divinity Cafe": ["fruit", "brunch", "sandwich", "salad", "dessert", "vegetarian", "grilled cheese", "tomato soup", "stir fry", "wraps"],
			   "Dolce Vita": ["sandwich", "salad", "dessert"],
			   "Freeman Center": ["sandwich", "salad", "dessert", "mac 'n cheese", "macaroni"],
			   "Ginger and Soy": ["asian", "bowls", "rice", "chicken", "dumplings", "poke bowl"],
			   "Gyotaku": ["asian", "sushi", "fish"],
			   "Il Forno": ["italian", "pizza", "pasta", "subs", "salad"],
			   "JB's Roasts and Chops": ["steak", "meat", "chops", "roasts", "fish"],
			   "Joe Van Gogh": ["coffee", "pastries", "dessert", "tea"],
			   "Loop Pizza Grill": ["bar", "beer", "french fries", "vegetarian", "soup", "hamburg", "fries", "loop", "pizza", "pasta", "salad", "sandwich", "appetizers", "snacks"],
			   "Marketplace": ["salad", "sandwich"],
			   "McDonald's": ["french fries", "shake", "shakes", "hamburgers", "fries", "fast food"],
			   "Nasher": ["salad", "soup", "sandwich", "brunch", "eggs", "fruit"],
			   "Panda": ["tofu", "asian", "orange chicken", "fried rice", "rice", "steak", "egg roll", "spring roll", "dupling"],
			   "Quenchers": ["smoothie", "smoothies", "nuts"],
			   "Red Mango": ["yogurt", "frozen yogurt", "smoothie", "smoothies", "fruit"],
			   "Saladelia": ["salad", "sandwich", "coffee", "pastries", "cheese", "crackers"],
			   "Sprout": ["vegetarian", "vegetables", "tofu", "vegan"],
			   "Tandoor": ["indian", "curry", "chicken", "vegetables", "vegetarian"],
			   "Terrace Cafe": ["sandwich", "soup", "beverages"],
			   "The Chef's Kitchen": ["fancy", "steak", "fish", "chicken", "salad"],
			   "The Commons": ["fancy", "steakhouse", "meat"],
			   "The Devil's Krafthouse": ["bar", "beer", "hamburger", "fries", "french fries", "drinks"],
               "The Farmstead": ["chicken", "beans", "steak", "salad", "sandwich", "carving", "turkey", "salmon", "ham", "soup"],
               "The Skillet": ["southern", "eggs", "chicken", "pork", "pulled pork", "mac and cheese", "beans", "collard greens", "dirty rice", "pudding"],
               "Trinity Cafe": ["sandwich", "salad", "sushi", "coffee"],
               "Twinnie's": ["sandwich", "soup", "salad", "coffee", "panini"]
            }

locations = {"Au Bon Pain": "416 Chapel Dr.",
			 "Bella Union": "204 Wannamaker Dr, Level 0, McClendon Tower, Duke University"
			 "Blue Express": "450 Research Dr, Durham, NC 27705",
			 "Cafe": "416 Chapel Dr, Durham",
			 "Cafe at Smith Warehouse": "114 S Buchanan Blvd",
			 "Cafe De Novo": "210 Science Dr, Durham",
			 "Cafe Edens": "416 Chapel Dr.",
			 "Dame's Express": "416 Chapel Dr.",
			 "Divinity Cafe": "416 Chapel Dr.",
			 "Dolce Vita": "416 Chapel Dr.",
			 "Freeman Center": "416 Chapel Dr.",
			 "Ginger and Soy": "416 Chapel Dr, Durham",
			 "Gyotaku": "416 Chapel Dr, Durham",
			 "Il Forno": "416 Chapel Dr, Durham",
			 "JB's Roasts and Chops": "416 Chapel Dr, Durham",
			 "Joe Van Gogh": "416 Chapel Dr.",
			 "Loop Pizza Grill": "416 Chapel Dr.",
			 "Marketplace": "416 Chapel Dr.",
			 "McDonald's": "416 Chapel Dr.",
			 "Nasher": "416 Chapel Dr.",
			 "Panda": "416 Chapel Dr.",
			 "Quenchers": "416 Chapel Dr.",
			 "Red Mango": "416 Chapel Dr.",
			 "Saladelia": "416 Chapel Dr.",
			 "Sprout": "416 Chapel Dr, Durham",
			 "Tandoor": "416 Chapel Dr, Durham",
			 "Terrace Cafe": "416 Chapel Dr.",
			 "The Chef's Kitchen": "416 Chapel Dr, Durham",
			 "The Commons": "416 Chapel Dr, Durham",
			 "The Devil's Krafthouse": "416 Chapel Dr, Durham",
             "The Farmstead": "416 Chapel Dr, Durham",
             "The Skillet": "416 Chapel Dr, Durham",
             "Trinity Cafe": "416 Chapel Dr.",
             "Twinnie's": "416 Chapel Dr."
            }

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
            values = restaurants[name]
            location = locations[name]

            dayOne = time_data[timeIndex]
            dayOneStart, dayOneEnd = clean_date(dayOne.text, dates[0])

            #IMPORTANT
            #To store in DB, use unicode(dayOneStart), and then str(that) if you need to

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
