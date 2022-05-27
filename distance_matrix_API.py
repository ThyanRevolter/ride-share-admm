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
