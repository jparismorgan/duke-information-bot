from google.appengine.ext import ndb
import re

# actions = {
#     'getBuilding': get_building,
#     'getFood': get_food,
#     'getEvent': get_event,
#     'getPerson': get_person,
#     'getDirections': get_directions
# }

class Restaurants(ndb.Model):
    name = ndb.StringProperty()
    hours = ndb.StringProperty()
    date = ndb.StringProperty()

class Triples(ndb.Model):
    subject = ndb.StringProperty()
    predicate = ndb.StringProperty()
    object = ndb.StringProperty()

def insert():
    r = Restaurants(name='PandaTwo', hours='11:00am-9:00pm')
    k = r.put()
    q = Restaurants.query()
    q = q.filter(Restaurants.name == 'PandaTwo')
    return str(q.get())

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
    q = q.filter(Triples.subject == subject, Triples.predicate == predicate, Triples.object == object)
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
    address = get_objects(subject=place, predicate="location").get()
    return address

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


#
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
# def get_food(request):
#     context = request['context']
#     entities = request['entities']
#
#     food = first_entity_value(entities, 'food')
#     if food:
#         food_name = sanitize_input(food)
#         restaurants = get_restaurants(food_name)
#         context['food'] = food_name
#         content['restaurants'] = restaurants
#
#         if context.get('missingFood') is not None:
#             del context['missingFood']
#     else:
#         context['missingFood'] = True
#         if context.get('food') is not None:
#             del context['food']
#
#     return context


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