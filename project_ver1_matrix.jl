using LinearAlgebra

A = rand(5,5)
A = A'*A
for i = 1:size(A)[1]
    for j = 1:size(A)[2]
        if i == j
            A[i,j] = 0
        end
    end
end

A

u= [1, 0, 0, 0, 0]
v = [0, 1, 0, 0, 0]

u= [1, 0, 0, 0, 0]
v = [0, 1, 0, 0, 0]


