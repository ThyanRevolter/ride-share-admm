using HTTP, JSON

origin = "37.4243691,-122.1597759"
destination = "37.4258662,-122.1609591"

# Input should be latitude and longitude
# Return Time, Distance
function findTimeDistance(origin,destination)
    api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"*"origins="*origin*"&destinations=" *destination *"&key="*api_key
    r = HTTP.request("GET", url)
    body_string = (String(r.body))
    parsed_data = JSON.parse(body_string)
    return parsed_data["rows"][1]["elements"][1]["distance"]["value"] #parsed_data["rows"][1]["elements"][1]["duration"]["value"], 
end

findTimeDistance(origin, destination)


function findElevation(location)
    api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"
    elevation_url = "https://maps.googleapis.com/maps/api/elevation/json?locations="*location*"&key="*api_key
    r = HTTP.request("GET", elevation_url)
    body_string = (String(r.body))
    parsed_data = JSON.parse(body_string)
    return parsed_data["results"][1]["elevation"]
end

findElevation(origin)