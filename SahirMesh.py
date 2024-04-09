# Sahir's wack ass mesh code

import random
import time

rows = 5
columns = 5
random.seed(time.time())
#0 = healthy cell
#1 = immune cell
#2 = cancer cell

mesh = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(random.randint(0, 2))
    mesh.append(row)
print(mesh)