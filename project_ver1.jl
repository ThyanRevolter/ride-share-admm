using LinearAlgebra
using HTTP, JSON
include("distance_matrix_API.jl")

# location 1 quillen
p1 = "37.42608322860995,-122.1588178069173"

# location 2 Oak creek
p2 = "37.43232913771922,-122.18699513497546"

# location 3 HP garage 
p3 = "37.443228634712966,-122.15464077643587"

# location 4 Goodwill
p4 = "37.41794560488438,-122.126188456268"

# location of car SLAC
c = "37.42004765994148,-122.20270570225145"


api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"


function getDirection(origin, destination)
    api_key = "AIzaSyCH6v-2T8u7wKKwluiX4FWUyOxcpvmTyD4"
    directionURL = "https://maps.googleapis.com/maps/api/directions/json?origin="*origin*"&destination="*destination*"&key="*api_key
    r = HTTP.request("GET", directionURL)
    body_string = (String(r.body))
    parsed_data = JSON.parse(body_string)
    return parsed_data
end

locations = [c, p1, p2, p3, p4]

function createDistanceMatrix(locations)
    n = length(locations)
    D = zeros(length(locations), length(locations))
    T = zeros(length(locations), length(locations))
    for i = 1:n
        for j = 1:n
            if i!=j                
                T[i,j], D[i,j] = findTimeDistance(locations[i], locations[j])
            end
        end
    end
    return T, D
end


T, D = createDistanceMatrix(locations)

T
D
S = D./T
S[findall(x->x==NaN, S)] .= 0 
diag(S) .= 0




data = getDirection(p1,p2)["routes"][1]
data["legs"][1]
length(data["legs"][1]["steps"])



counter = 1
for i in data["legs"][1]["steps"]
    println(counter, " Step")
    for j in i
        println("Step attribute")
        println(j)
        println()
    end
    counter = counter + 1
end


JSON.print(data)


# # URL for Speedlimit 

# function getSpeedLimit(origin,destination)
#     api_key = "AIzaSyCafK13zizgMdihUc_I_dsjlVgeWkI9TrA"
#     directionURL = "https://roads.googleapis.com/v1/speedLimits?path="*origin*"|"*destination*"&key="*api_key
#     r = HTTP.request("GET", directionURL)
#     body_string = (String(r.body))
#     parsed_data = JSON.parse(body_string)
#     return parsed_data
# end

# speed_limit_data = getSpeedLimit(p1,p2)

# # URL for Direction
# directionURL = "https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key="

# # URL for snap to roads
# snapRoad = "https://roads.googleapis.com/v1/snapToRoads?parameters&key=YOUR_API_KEY"

# speedLimit = "https://roads.googleapis.com/v1/speedLimits?path="
