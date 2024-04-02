# Sahir's mesh code

import random
import time

rows = 40
columns = 40
mesh = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(0);
    mesh.append(row)
print(mesh)
mesh[0][2] = 5
print(mesh)