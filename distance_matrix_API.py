import requests, json, numpy as np

# Provide origin and destination and the output is a tuple of time and distance between the origin and destination 
def get_distance(origin, destination):
    api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"+"origins="+origin+"&destinations=" +destination +"&units=imperial&key="+api_key
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return result["rows"][0]["elements"][0]['duration']['value'], result["rows"][0]["elements"][0]['distance']['value']


# # location 1 quillen
# p1 = "37.42608322860995,-122.1588178069173"

# # location 2 Oak creek
# p2 = "37.43232913771922,-122.18699513497546"

# # location 3 HP garage 
# p3 = "37.443228634712966,-122.15464077643587"

# # location 4 Goodwill
# p4 = "37.41794560488438,-122.126188456268"

# # location of car SLAC
# c = "37.42004765994148,-122.20270570225145"

# locations = [c, p1, p2, p3, p4]


# pass a string list of n number of location's latitude and longitude 
def createDistanceMatrix(locations):
    n = len(locations)
    D = np.zeros((n,n))
    T = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i!=j and j != 0:               
                T[i,j], D[i,j] = get_distance(locations[i], locations[j])
    return T, D

#T, D = createDistanceMatrix(locations)
