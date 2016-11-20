####################################################################################################
######## Written for HackDuke 2016
######## Credit must be given to Kevin He of TabDuke for the scraping format and code architecture
####################################################################################################

import requests
import json
import datetime
import math
import logging
import pytz

desiredStops = ["4117202", "4146366", "4158202", "4098210", "4177628", "4177630",
    "4098226", "4098230", "4158230", "4177632", "4157330", "4151494", "4098294", "4098298", "4098394", "4098218"]

desiredStopNames = {
    4098394: 'Campus Walk/LaSalle South',
    4098218: "Research Dr at Duke Clinic",
    4098210: "Science Drive Circle",
    4098226: "Flowers Drive Southbound",
    4098230: "Flowers Drive Northbound",
    4117202: "East Campus Quad",
    4146366: "Duke Chapel",
    4151494: "Swift Ave at Campus Dr Eastbound",
    4157330: "Swift/Campus Westbound",
    4158202: "Gilbert-Addoms Westbound",
    4158230: "Smith Warehouse Westbound",
    4177628: "Campus/Anderson Westbound",
    4177630: "Campus/Anderson Eastbound",
    4177632: "Smith Warehouse Eastbound",
    4098298: "Alexander Ave at Pace St Westbound",
    4098294: "Alexander Ave at Pace St Eastbound"
}

stopOrder = [
    "Duke Chapel",
    "East Campus Quad",
    "Alexander/Pace Westbound",
    "Alexander/Pace Eastbound",
    "Campus Walk/LaSalle South",
    "Research Dr at Duke Clinic",
    "Science Drive Circle",
    "Gilbert-Addoms Westbound",
    "Smith Warehouse Eastbound",
    "Smith Warehouse Westbound",
    "Campus/Anderson Eastbound",
    "Campus/Anderson Westbound",
    "Flowers Drive Southbound",
    "Flowers Drive Northbound",
    "Swift/Campus Eastbound",
    "Swift/Campus Westbound"
]

altStopNames = {
    "Swift Ave at Campus Dr Eastbound": "Swift/Campus Eastbound",
    "Alexander Ave at Pace St Eastbound": "Alexander/Pace Eastbound",
    "Alexander Ave at Pace St Westbound": "Alexander/Pace Westbound"
}

DUKE_AGENCY_ID = '176';

activeBuses = []
activeBusNames = {}
stopArrivals = {}

def getBusTimes():
    url ='https://transloc-api-1-2.p.mashape.com/routes.json?agencies=' + DUKE_AGENCY_ID + '&callback=call'
    headers = {'X-Mashape-Key': 'dbkV9N1yxOmsh7i5mjx21iNKfRDvp1qe8Q1jsnjGV0MEemwXqd', "Accept": "application/json"}
    resp = requests.get(url, headers = headers)
    data = resp.json()
    route_list = data['data']['176']

    for i in range(len(route_list)):
        activeBuses.append(route_list[i]['route_id'])

        activeBusNames[route_list[i]['route_id']] = {
            "name": route_list[i]["long_name"],
            "stops": route_list[i]["stops"]
        }

    routesRequest = generateRoutesQuery();
    stopsRequest = generateStopsQuery();

    #Now get the estimated arrival times
    url = 'https://transloc-api-1-2.p.mashape.com/arrival-estimates.json?agencies=' + DUKE_AGENCY_ID + '&callback=call'  + '&routes=' + routesRequest + '&stops=' + stopsRequest
    headers2 = {'X-Mashape-Key': 'dbkV9N1yxOmsh7i5mjx21iNKfRDvp1qe8Q1jsnjGV0MEemwXqd', "Accept": "application/json"}
    resp = requests.get(url, headers=headers2)
    data = resp.json()

    #set up possible arrival times
    for i in range(len(data['data'])):
        arrival_list = data['data'][i]['arrivals']
        buses_arriving = []
        for bus in arrival_list:
           # print activeBusNames[bus["route_id"]]["name"]
            buses_arriving.append({
                "name":activeBusNames[bus["route_id"]]["name"],
                "arrival": bus["arrival_at"]
            })
        if int(data['data'][i]["stop_id"]) in desiredStopNames.keys():
            key = int(data['data'][i]["stop_id"])
            stopArrivals[desiredStopNames[key]] = {
                "routes": buses_arriving
            }

    arrivalEstimates = {}

    #estimate arrival times
    logging.info(str(stopArrivals))
    for stop in stopArrivals:


        if stop not in arrivalEstimates.keys():
            arrivalEstimates[stop] = {}

        routes = stopArrivals[stop]["routes"]
        for route in routes:
            if route["name"] not in arrivalEstimates[stop]:
                arrivalEstimates[stop][route["name"]] = []
            #hacky to convert to datetime. careful with the -6
            arrival = datetime.datetime.strptime(route["arrival"][:-6], '%Y-%m-%dT%H:%M:%S')

            logging.info(arrival)

            localtz = pytz.timezone('America/New_York')
            arrival = localtz.localize(arrival)

            logging.info(arrival)

            logging.info(datetime.datetime.now())

            fromNow = arrival - datetime.datetime.now(pytz.timezone('America/New_York'))

            logging.info(fromNow)

            logging.info(datetime.datetime.now(pytz.timezone('America/New_York')))

            minutesFromNow = math.floor(fromNow.total_seconds()/float(60) )

            logging.info(minutesFromNow)

            arrivalEstimates[stop][route["name"]].append(minutesFromNow)

    #get the next two arrival times for the busses
    stops = []
    buses = {}
    logging.warning(str(arrivalEstimates))
    for stop in arrivalEstimates:
        routes = arrivalEstimates[stop]
        if stop in altStopNames:
            stop = altStopNames[stop]
        stops.append(stop)
        buses[stop] = []
        for route in routes:
            times = routes[route]
            if len(times) >= 2:
                times = [times[0], times[1]]
            elif len(times) == 0:
                times = ['Out of service']
            timeString = ''
            for i in range(len(times)):
                if times[i] <= 0:
                    times[i] = '<1'
                timeString += str(times[i])
                if (i < len(times) - 1):
                    timeString += ' & '

        timeString += ' min.'

        buses[stop].append({
            "route": route,
            "times": timeString,
        })

    #now iterate through.. check once transloc is back online
    temp = []
    for i in range(len(stopOrder)):
        if stopOrder[i] in stops:
            temp.append(stopOrder[i])

    ret_string = ""
    for stop in buses:
        ret_string += stop + "\n"
        for index, bus in enumerate(buses[stop]):
            ret_string += buses[stop][index]["route"] + ': ' +buses[stop][index]["times"] + '\n'
        # for bus in temp[stop]:
        #     temp = bus[0]
            #ret_string += temp

    #return str(arrivalEstimates) + '||||' + str(stopArrivals) + '||||' + str(data)
    return ret_string
    # print temp
    # print buses

def generateRoutesQuery():
    query = ""
    for index, q in enumerate(activeBuses):
        query += str(q)
        if index != len(activeBuses) - 1:
            query += "%2C"
    return query

def generateStopsQuery():
    query = ""
    for index, q in enumerate(desiredStops):
        query += str(q)
        if index != len(desiredStops) - 1:
            query += "%2C"
    return query
