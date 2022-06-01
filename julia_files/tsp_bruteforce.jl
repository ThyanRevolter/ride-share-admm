using LinearAlgebra

include("project_ver1.jl")

n_comb = 4
path_dict = Dict("x" =>0)
counter = 0
for i = 1:n_comb, j = 1:n_comb, k = 1:n_comb, l = 1:n_comb
    if i != j && i != k && i != l && j != k && j != l && k != l
        println("i = ", i,"j = ", j,"k = ", k,"l = ", l)
        path = string(i,j,k,l)
        path_dict = merge(path_dict, Dict(path => (D[1,i+1] + D[i+1,j+1] + D[j+1,k+1] + D[k+1,l+1])))
    end
end
delete!(path_dict, "x")
min_dist = minimum(values(path_dict))
findmin(path_dict)[2]




