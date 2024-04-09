class Patient:
    def __init__(self):
        self.state = 0
        self.healRate = 0
        self.infectRate = 0.5
        self.vacRate = 0.05

    def runPerc(self, rate):
        self.rate = rate
        if random.random() < self.rate:
            return True
        else:
            return False

import random

#Creates a population with the set parameters of size-------------------------------------------------------------------
rows = 10
columns = 30
population = rows * columns

mesh = []
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(Patient())
    mesh.append(row)


#Calculates the Initial amount of infected persons and adds them to the population--------------------------------------
initialInfecPerc = 0.2
initialInfec = int(population * initialInfecPerc)

for i in range(initialInfec):
    x = random.randrange(rows)
    y = random.randrange(columns)
    mesh[x][y].state = 1

#Iterations for Simulation----------------------------------------------------------------------------------------------
iter = 100

for i in range(iter):

    for x in range(rows):
        for y in range(columns):

            if mesh[x][y].state == 2: #Checks if Patient is vaccinated
                pass

            elif mesh[x][y].state == 0: #Checks for healthy Patient
                if i >= int(iter/2): #Checks to see if iterations are halfway done
                    if mesh[x][y].runPerc(mesh[x][y].vacRate):
                        mesh[x][y].state = 2
                        mesh[x][y].healRate = 1.0
                        mesh[x][y].infectRate = 0

            elif mesh[x][y].state == 1:
                if mesh[x-1][y].state == 0: #Infects Cell above
                    if mesh[x][y].runPerc(mesh[x][y].infectRate):
                        mesh[x-1][y].state = 1
                if (x <= rows-2) and mesh[x+1][y].state == 0: #Infects Cell Below
                    if mesh[x][y].runPerc(mesh[x][y].infectRate):
                        mesh[x+1][y].state = 1
                if mesh[x][y-1].state == 0: #Infects Cell to Left
                    if mesh[x][y].runPerc(mesh[x][y].infectRate):
                        mesh[x][y-1].state = 1
                if (y <= rows-2) and mesh[x][y+1].state == 0: #Infects Cell to right
                    if mesh[x][y].runPerc(mesh[x][y].infectRate):
                        mesh[x][y+1].state = 1

                if mesh[x][y].runPerc(mesh[x][y].healRate): #Gives the cell a chance to heal
                    mesh[x][y].state = 0
                    mesh[x][y].healRate = 0
                    mesh[x][y].infectRate = 0.3
                else: #If the cell is still sick, makes the cell recover
                    mesh[x][y].healRate += 0.1
                    mesh[x][y].infectRate -= 0.05


#Test Print-------------------------------------------------------------------------------------------------------------
    for x in range(rows):
        for y in range(columns):
            print(mesh[x][y].state, end="")
        print("")
    print("")



