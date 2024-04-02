# Sahir's mesh code

import random
import time

rows = 5
columns = 5
random.seed(time.time())

mesh = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(random.randint(0, 2))
    mesh.append(row)
print(mesh)