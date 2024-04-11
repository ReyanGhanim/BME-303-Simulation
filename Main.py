import tkinter as tk
import random
import csv
import matplotlib.pyplot as plt
import os
from PIL import Image

#The Patient class creates Patient objects that will be put into the mesh
class Patient:
    def __init__(self):
        self.state = 0  #State 0 is healthy, state 1 is sick, state 2 is vaccinated
        self.healRate = 0   #Patients start with a default healRate of 0 (because they start as healthy)
        self.infectRate = 0.2   #Patients start with a default infectRate of 0.2 that will become useful once the patient is sick
        self.vacRate = 0.05     #Patients start with a vaccination rate of 0.05, which comes into effect halfway through the simulation

    #The runPerc (run percentage) function returns true or false when given a rate by using random.random() to generate a number between zero and one and comparing this to the given rate
    def runPerc(self, rate):
        if random.random() < rate:
            return True
        else:
            return False

#The get_color function accesses a Patient's data and returns a color associated with their state
def get_color(Patient):
    if Patient.state == 0:
        return "white"
    elif Patient.state == 1:
        if Patient.healRate == 0:
            return "darkred"
        elif Patient.healRate == 0.1:
            return "firebrick"
        elif Patient.healRate == 0.2:
            return "red"
        elif Patient.healRate == 0.3:
            return "indianred"
        else:
            return "lightcoral"
    elif Patient.state == 2:
        return "green"
    else:
        return "black"

#update_grid is a function used between iterations to update the color of the boxes in the simulation
def update_grid():
    for x in range(rows):
        for y in range(columns):
            cells[x][y].configure(bg=get_color(mesh[x][y]))

#The count_states function uses a dictionary to count the number of each Patient type/state in the mesh
def count_states():
    counts = {0: 0, 1: 0, 2: 0}
    for row in mesh:
        for patient in row:
            counts[patient.state] += 1
    return counts

#The simulate function is the most important function which sets up the simulation and implements Patient-to-Patient interactions during the simulation
def simulate(iteration=0):
    #The first 5 seconds of the simulation display the first iteration
    if iteration == 0:
        update_grid()  # Update the grid to display the initial state
        root.after(5000, simulate, iteration + 1)
    #The elif statement runs for the rest of the iterations past the first iteration
    elif iteration < iterations:
        for x in range(rows):
            for y in range(columns):
                patient = mesh[x][y]
                if patient.state == 2:  # If patient is vaccinated (state 2), nothing happens (continue)
                    pass
                elif patient.state == 0:  # If patient is healthy (state 0), the simulation is past halfway done, and runPerc (the chance to get vaccinated) returns positive, the patient becomes vaccinated and their attributes are updated to reflect this
                    if iteration >= iterations // 2 and patient.runPerc(patient.vacRate):
                        patient.state = 2
                        patient.healRate = 1.0
                        patient.infectRate = 0
                elif patient.state == 1:  # If patient is infected (state 1), the surrounding cells are potentially infected using the runPerc function and the patient's infection rate. Indexes out of range are ignored
                    if x != 0 and mesh[x - 1][y].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x - 1][y].state = 1
                    if x < rows - 1 and mesh[x + 1][y].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x + 1][y].state = 1
                    if y != 0 and mesh[x][y - 1].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x][y - 1].state = 1
                    if y < columns - 1 and mesh[x][y + 1].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x][y + 1].state = 1
                    # The patient is given a chance to become healthy using the runPerc function and the patient's heal rate
                    if patient.runPerc(patient.healRate):
                        patient.state = 0
                        patient.healRate = 0
                        patient.infectRate = 0.3
                    # If the patient doesn't become healthy, their chances to become healthy increase and their chances to infect others decreases
                    else:
                        patient.healRate += 0.1

        #Updates the grid every iteration
        update_grid()
        counts = count_states()
        #Writes the number of patients of each type to the CSV file for later usage in the plot
        data_writer.writerow([iteration, counts[0], counts[1], counts[2]])

        # Create an image of the grid
        img = Image.new('RGB', (columns, rows))
        pixels = img.load()
        for x in range(rows):
            for y in range(columns):
                color = get_color(mesh[x][y])
                pixels[y, x] = {
                    "white": (255, 255, 255),
                    "darkred": (139, 0, 0),
                    "firebrick": (178, 34, 34),
                    "red": (255, 0, 0),
                    "indianred": (205, 92, 92),
                    "lightcoral": (240, 128, 128),
                    "green": (0, 128, 0),
                    "black": (0, 0, 0)
                }[color]

        # Save the image to a new file
        img.save(f'grids/grid_{iteration}.png')
        root.after(100, simulate, iteration + 1)
    else:
        #Closes the CSV file after the simulation is done
        data_file.close()

#The main function
if __name__ == "__main__":
    os.makedirs('grids', exist_ok=True)
    root = tk.Tk()
    root.title("Disease Spread Simulation")

    #Implements a 50x50 mesh
    rows, columns = 50, 50
    cell_size = 15
    mesh = [[Patient() for _ in range(columns)] for _ in range(rows)]
    cells = [[tk.Frame(root, bg="white", width=cell_size, height=cell_size) for _ in range(columns)] for _ in range(rows)]

    for x in range(rows):
        for y in range(columns):
            cells[x][y].grid(row=x, column=y)
            cells[x][y].pack_propagate(False)

    #10% of the population will be infected when the simulation starts. The patients are randomly chosen
    initialInfecPerc = 0.1
    initialInfec = int(rows * columns * initialInfecPerc)
    infected_cells = random.sample([(x, y) for x in range(rows) for y in range(columns)], initialInfec)
    for x, y in infected_cells:
        mesh[x][y].state = 1

    #The simulation has 150 total iterations
    iterations = 150

    #Writes a simulation_data csv that stores the patient counts of each type for each iteration
    data_file = open('simulation_data.csv', 'w', newline='')
    data_writer = csv.writer(data_file)

    # Write initial state (iteration 0) to CSV file
    initial_counts = count_states()
    data_writer.writerow([0, initial_counts[0], initial_counts[1], initial_counts[2]])

    simulate()  # Start the animation

    root.mainloop()

    # Opens the simulation_data csv and saves the patient counts of each type (healthy, sick, vaccinated) for each iteration to lists
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

    # Plotting the results using the healthy, infected, and vaccinated lists from the csv file
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