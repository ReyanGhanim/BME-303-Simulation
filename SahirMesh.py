# Sahir's wack ass mesh code

import random
import time

rows = 5
columns = 5
random.seed(time.time())
#0 = healthy cell
#1 = immune cell
#2 = cancer cell

#Creates a population with the set parameters of size-------------------------------------------------------------------
rows = 5
columns = 5
population = rows * columns

mesh = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(0)
    mesh.append(row)

mesh[3][-1] = 1

for x in range(rows):
    for y in range(columns):
        print(mesh[x][y], end="")
    print("")
print("")