# New Customer Data
# Palm drive
new_cust = "37.429070511839086,-122.16979819313977"

left_top_lat = 37.470992059291454
left_top_long = -122.26384676573207
right_bottom_lat = 37.41590660664082
right_bottom_long = -122.15556246814724

import random
import numpy as np

def get_location_list(coordindates):
    n = coordindates.shape[1]
    location = []
    for i in range(n):
        location.append(str(coordindates[0,i])+','+str(coordindates[1,i]))
    return location

# generate N car and random passengers
def generate_cars(N):
    cars_dict = dict()
    for i in range(N):
        n = random.randint(3,5)
        lat_list = np.array([random.uniform(right_bottom_lat, left_top_lat) for i in range(n) ])
        long_list = np.array([random.uniform(left_top_long, right_bottom_long) for i in range(n) ])
        cars_dict["car"+str(i)]= np.vstack((lat_list, long_list))

    location_list = []
    for val in cars_dict.values():
        location_list.append(get_location_list(val))
    return location_list


class car:
    def __init__(self, c_pick, c_drop, c_t, p1_pick, p1_drop, p1_t, p2_pick, p2_drop, p2_t, p3_pick, p3_drop, p3_t):
        self.c_pick = c_pick
        self.c_drop = c_drop
        self.c_t = c_t
        self.p1_pick = p1_pick
        self.p1_drop = p1_drop
        self.p1_t = p1_t
        self.p2_pick = p2_pick
        self.p2_drop = p2_drop
        self.p2_t = p2_t
        self.p3_pick = p3_pick
        self.p3_drop = p3_drop
        self.p3_t = p3_t



# def main():
#     left_top_lat = 37.470992059291454
#     left_top_long = -122.26384676573207
#     right_bottom_lat = 37.41590660664082
#     right_bottom_long = -122.15556246814724

# # Car 1 and riders information
# # location of car SLAC
# c1 = "37.42004765994148,-122.20270570225145"

# # location 1 quillen
# p1_1 = "37.42608322860995,-122.1588178069173"

# # location 2 Oak creek
# p2_1 = "37.43232913771922,-122.18699513497546"

# # location 3 HP garage 
# p3_1 = "37.443228634712966,-122.15464077643587"

# # # location 4 Goodwill
# # p4_1 = "37.41794560488438,-122.126188456268"

# locations_1 = [c1, p1_1, p2_1, p3_1]

# # Car 2 and riders information
# # location of car 2 Rains house
# c2 = "37.421865594825,-122.15812606214956"

# # location 1 telliferic barcelona
# p1_2 = "37.42608322860995,-122.1588178069173"

# # location 2 Apple store palo alto
# p2_2 = "37.446597506095806,-122.16078403912387"

# # location 3 Stratford School
# p3_2 = "37.44153772568974,-122.13190277823341"

# locations_2 = [c2, p1_2, p2_2, p3_2]


# # Car 3 and riders information
# # location of car 3 peer's park
# c3 = "37.43195323694237,-122.14754000985644"

# # location 1 Johnson park
# p1_3 = "37.44945694596284,-122.16311968010169"

# # location 2 Stanford Shopping Center
# p2_3 = "37.44421618424591,-122.17157666303187"

# # location 3 St. Patrick's Seminary & University
# p3_3 = "37.46078690151287,-122.16792127263804"

# locations_3 = [c3, p1_3, p2_3, p3_3]

# # car 4 and rider's information
# # location of car 4 VA Palo Alto Health Care System
# c4 = "37.40601417002996,-122.14105598274075"

# # location 1 Elizabeth F. Gamble Garden
# p1_4 = "37.43862411403473,-122.14830762649643"

# # location 2 Googleplex
# p2_4 = "37.422844469597,-122.08502055320061"

# locations_4 = [c4, p1_4, p2_4]
