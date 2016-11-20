from google.appengine.ext import ndb
import re
import BusScraper

class Restaurants(ndb.Model):
    name = ndb.StringProperty()
    hours = ndb.StringProperty()
    date = ndb.StringProperty()
    value = ndb.StringProperty()

class Triples(ndb.Model):
    subject = ndb.StringProperty()
    predicate = ndb.StringProperty()
    object = ndb.TextProperty()

def updateRestaurants():

    return "Done"

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def get_objects(subject, predicate):
    subject = sanitize_input(subject)
    predicate = sanitize_input(predicate)
    q = Triples.query()
    q = q.filter(Triples.subject == subject, Triples.predicate == predicate)
    return q

def get_subjects(predicate, object):
    predicate = sanitize_input(predicate)
    q = Triples.query()
    q = q.filter(Triples.object == object, Triples.predicate == predicate)
    return q

def create_tuple(subject, predicate, object):
    q = Triples.query()
    subject = sanitize_input(subject)
    predicate = sanitize_input(predicate)
    q = q.filter(Triples.subject == subject)
    if q.count(1) > 0:
        t = q.get()
        t.subject = subject
        t.predicate = predicate
        t.object = object
    else:
        t = Triples(subject=subject,predicate=predicate,object=object)
    return t.put()


def sanitize_input(input):
    return re.sub('\s+', '', input).lower()


def get_location(place):
    '''
    Query DB and return addresses
    '''
    address = get_objects(subject=place, predicate="location")
    if(address is not None):
        return address.get()
    return ""

def find_location_of(request):
    context = request['context']
    entities = request['entities']

    loc = first_entity_value(entities, 'location')
    if loc:
        loc = sanitize_input(loc)
        context['foundLocation'] = get_location(loc)
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('foundLocation') is not None:
            del context['foundLocation']

    return context

def get_food_offerings(location):
    food = get_objects(subject=place, predicate="offering")
    if(food is not None):
        return food.get()
    return []

def get_offerings(request):
    context = request['context']
    entities = request['entities']

    loc = first_entity_value(entities, 'location')
    if loc:
        loc = sanitize_input(loc)
        context['offerings'] = get_location(loc)
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('foundLocation') is not None:
            del context['foundLocation']

    return context

def dukeSearch(request):
    context = request['context']
    entities = request['entities']
    query = first_entity_value(entities, 'search_phrase')
    str.replace(query, ' ', '%20')
    context['search_query'] = query
    return context

def createEvent(request):
    context = request['context']
    entities = request['entities']
    intent = entities['intent']
    datetime = entities['datetime']
    message_body = entities['search_query']
    location = entities['location']

    subject = sanitize_input(message_body)
    create_tuple(subject=subject, predicate="time", object=datetime)
    create_tuple(subject=subject, predicate="location", object=location)

    return context

def findEvent(request):
    context = request['context']
    entities = request['entities']

    return context


#
# def get_restaurants(food):
#     '''
#     Query DB and return restaurant names with addresses
#     '''
#
#
# def get_building(request):
#     context = request['context']
#     entities = request['entities']
#
#     loc = first_entity_value(entities, 'location')
#     if loc:
#         building = sanitize_input(loc)
#         context['building'] = building
#         #content['address'] = get_address(building)
#         if context.get('missingBuilding') is not None:
#             del context['missingBuilding']
#     else:
#         context['missingBuilding'] = True
#         if context.get('building') is not None:
#             del context['building']
#
#     return context
#
#
def get_food(request):
    context = request['context']
    entities = request['entities']

    food = first_entity_value(entities, 'food')
    if food:
        food_name = sanitize_input(food)
        restaurants = get_location(food_name)
        context['food'] = food_name
        context['restaurants'] = restaurants

        if context.get('missingFood') is not None:
            del context['missingFood']
    else:
        context['missingFood'] = True
        if context.get('food') is not None:
            del context['food']

    return context

def dukeSearch(request):
    context = request['context']
    entities = request['entities']
    query = first_entity_value(entities, 'search_phrase')
    if query != None:
        str.replace(query, ' ', '%20')
    context['search_query'] = query
    return context


def getBusTimes(request):
    context = request['context']
    entities = request['entities']
    return_string = BusScraper.getBusTimes()
    if return_string != None:
        context['bus_times'] = return_string
    else:
        context['bus_times'] = "There seems to be a problem with Transloc. We will ask Samuel Jackson and get back to you."
    return context


# def get_event(request):
#     context = request['context']
#     entities = request['entities']
#
#     loc = first_entity_value(entities, 'location')
#     if loc:
#         location = sanitize_input(loc)
#         context['location'] = location
#         date_time = first_entity_value(entities, 'dateTime')
#         if date_time:
#             content['datetime'] = get_date_time(date_time)
#             if context.get('missingDateTime') is not None:
#                 del context['missingDateTime']
#
#     else:
#         date_time = first_entity_value(entities, 'dateTime')
#         if date_time:
#
#         else:
#
#         context['missingDateTime'] = True
#         if context.get('dateTime') is not None:
#             del context['dateTime']
#
#     return context
#
#
# def get_person_location(name):
#     '''
#     Query DB and return location of person with name
#     '''
#
#
# def get_person(request):
#     context = request['context']
#     entities = request['entities']
#
#     person = first_entity_value(entities, 'person')
#     if person:
#         person_name = sanitize_input(food)
#         context['name'] = person_name
#         content['location'] = get_person_location(person_name)
#
#         if context.get('missingName') is not None:
#             del context['missingName']
#     else:
#         context['missingName'] = True
#         if context.get('name') is not None:
#             del context['name']
#
#     return context