import matplotlib.pyplot as plt

infile = open("simulation_data.csv", "r")

currentLine = []
healthy = []
infected = []
vaccinated = []
for line in infile:
    line = line.rstrip("\n")
    currentLine = line.split(",")
    healthy.append(int(currentLine[1]))
    infected.append(int(currentLine[2]))
    vaccinated.append(int(currentLine[3]))
infile.close()
print(healthy)
print(infected)
print(vaccinated)

#Plotting the results
plt.xlim(0, len(healthy))
plt.ylim(0, max(healthy))
plt.plot(healthy, label='Healthy')
plt.plot(infected, label='Infected')
plt.plot(vaccinated, label='Vaccinated')
plt.xlabel('Time (weeks)')
plt.ylabel('Number of Individuals')
plt.title('Meningitis Curve')
plt.legend(loc='upper right')
plt.show()
