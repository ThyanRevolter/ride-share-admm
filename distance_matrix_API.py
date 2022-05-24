import requests, json

origin = "37.4243691%2C-122.1597759"
destination = "37.4258662%2C-122.1609591"
api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"
url = "https://maps.googleapis.com/maps/api/distancematrix/json?"+"origins="+origin+"&destinations=" +destination +"&units=imperial&key="+api_key
url = "https://maps.googleapis.com/maps/api/distancematrix/json?"*"origins="*origin*"&destinations=" *destination *"&units=imperial&key="*api_key

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
result = json.loads(response.text)
print("Distance between selected destnation is:"+ result["rows"][0]["elements"][0]['distance']['text'])