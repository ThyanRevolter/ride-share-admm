using LinearAlgebra, Random

# Consider size of a grid 100x100

# The distance between each nodes is given
grid_size = 100
grid_distance = 10*rand(grid_size,grid_size)
diag(grid_distance) .= 0 
grid_distance
# . 3m . 4m  . 5m . 8m . 1m . 2m . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .
# . . . . . . . . . .

n_riders = 40

# Generate source and destination nodes
source_coords = zeros(n_riders,2)
destination_coords = zeros(n_riders,2)

# Source node X axix
source_coords[:,1] = [Integer(round(grid_size*rand())) for i = 1:n_riders]
# destination Y Axis
source_coords[:,2] = [Integer(round(grid_size*rand())) for i = 1:n_riders]

# Source node X axix
destination_coords[:,1] = [Integer(round(grid_size*rand())) for i = 1:n_riders]
# destination Y Axis
destination_coords[:,2] = [Integer(round(grid_size*rand())) for i = 1:n_riders]



# Generate Vehicles

n_drivers = 10

# Initial location of the vehicles
initial_location = zeros(n_drivers,2)

for i = 1:n_drivers
    # initial driver location
    initial_location[i,1] = Integer(round(grid_size*rand()))
    initial_location[i,2] = Integer(round(grid_size*rand()))
end


