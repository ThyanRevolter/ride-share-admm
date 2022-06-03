from random import sample
import string
from typing import Dict
import numpy as np
from car_driver_data import *
from master_problem import *
from optimal_rollouts import *
from distance_matrix_API import * 
from optimal_dropoffs import Drop
import csv
import polyline

new_cust = "37.429070511839086,-122.16979819313977"
new_cust_drop = "37.4560780826105,-122.19403843683895"
location_list =  generate_cars(20)
feasible_cars_list, feasible_cars_keys = feasible_cars(new_cust, location_list)
energy = get_energy(new_cust, feasible_cars_list)
y, min_energy = solve_master(feasible_cars_list, energy)
print("Assigned Car Id is "+ feasible_cars_keys[np.argmax(y)])
print("Assigned Car location is "+ feasible_cars_list[np.argmax(y)][0])


energy_matrix_dict = dict()
car_location = []
for i in range(len(feasible_cars_list)):
    car_location.append(feasible_cars_list[i][0])
    feasible_cars_list[i][0] = new_cust
    feasible_cars_list[i].append(new_cust_drop)
    T_car, D_car = createDistanceMatrix(feasible_cars_list[i])
    energy_matrix_dict[feasible_cars_keys[i]] = get_energy_matrix(T_car, D_car)

sample_energy = []
drop_order_admm_dict = dict()
drop_order_rpp_dict = dict()

for energy_matrix in energy_matrix_dict:
    print(energy_matrix)
    print(energy_matrix_dict[energy_matrix].shape)
    print(energy_matrix_dict[energy_matrix])
    sample_energy = energy_matrix_dict[energy_matrix]
    drop = Drop(sample_energy)    
    drop_order_admm_dict[energy_matrix] = drop.drop_order(solver="nc-admm")
    drop_order_rpp_dict[energy_matrix] = drop.drop_order(solver="relax-round-polish")

header_column = ["Car Id", "Car Location", "Customer Location", "Customer Drop-Off", "Drop order 1", "Drop location 1", "Drop order 2", "Drop location 2", "Drop order 3", "Drop location 3", "Drop order 4", "Drop location 4","Polyline Encode"]

print(drop_order_admm_dict)
print()
rows=[]
poly_line_list =[]
counter = 0
for energy_matrix in energy_matrix_dict:
    car_list =[energy_matrix, car_location[counter],new_cust,new_cust_drop]
    poly_encoder = [car_location[counter], new_cust]
    for admm_order in drop_order_admm_dict[energy_matrix][1:]:
        car_list.append("customer"+str(admm_order))
        car_list.append(feasible_cars_list[counter][admm_order])
        poly_encoder.append(feasible_cars_list[counter][admm_order])
    poly_line_list.append(poly_encoder)
    rows.append(car_list)
    counter+=1

print("coordinate system")
poly_line_coords = []
for poly_line in poly_line_list:
    x,y = loc2xy(poly_line)
    coord =[]
    for i in range(len(x)):
        coord.append((y[i],x[i]))
    poly_line_coords.append(coord)

dir_url_list = []
for poly_line in poly_line_list:
    dir_url = r"https://www.google.com/maps/dir/'"+"'/'".join(poly_line)+"'/@37.4448723,-122.2264491,13z/"
    print(dir_url)
    dir_url_list.append([dir_url])

r"https://www.google.com/maps/dir/'37.44578437974878,-122.19105037292434'/'37.429070511839086,-122.16979819313977'/'37.42399075589427,-122.2201932030622'/'37.41861475034866,-122.1938395390148'/'37.4560780826105,-122.19403843683895'/'37.46020137652942,-122.21067640102834'/@37.4413518,-122.2283918,13z/data=!3m1!4b1!4m25!4m24!1m3!2m2!1d-122.1910504!2d37.4457844!1m3!2m2!1d-122.1697982!2d37.4290705!1m3!2m2!1d-122.2201932!2d37.4239908!1m3!2m2!1d-122.1938395!2d37.4186148!1m3!2m2!1d-122.1940384!2d37.4560781!1m3!2m2!1d-122.2106764!2d37.4602014"
r"https://www.google.com/maps/dir/'37.44091772680026,-122.18659683264175'/'37.429070511839086,-122.16979819313977'/'37.447952020019585,-122.25870972824714'/'37.4560780826105,-122.19403843683895'/'37.45874738009613,-122.22688355797511'/@37.4494811,-122.2837199,12z/data=!3m1!4b1!4m21!4m20!1m3!2m2!1d-122.1865968!2d37.4409177!1m3!2m2!1d-122.1697982!2d37.4290705!1m3!2m2!1d-122.2587097!2d37.447952!1m3!2m2!1d-122.1940384!2d37.4560781!1m3!2m2!1d-122.2268836!2d37.4587474"
print("Next is geojson")
from geojson import LineString, Feature, FeatureCollection, dump, utils
crs = {
    "type": "Name",
    "properties": {
        "name": "EPSG:3857"
    }
}
features = []
counter = 0
for coords in poly_line_coords:
    poly_line_string = Feature(geometry=LineString(coords))
    poly_line_string.properties["Car_ID"] = rows[counter][0]
    features.append(poly_line_string)
    counter += 1

feature_collection = FeatureCollection(features,crs=crs)
print("Is feature collection valid: ")
print(feature_collection.is_valid)
with open('car_path.geojson', 'w') as f:
   dump(feature_collection, f)

filename = "car_list_1.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(header_column) 
        
    # writing the data rows 
    csvwriter.writerows(rows)

print(dir_url_list)
filename = "direction_car_list.csv"
with open(filename, 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)        
    # writing the data rows 
    csvwriter.writerows(dir_url_list)
