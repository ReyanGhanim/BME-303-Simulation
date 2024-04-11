import tkinter as tk
import random
import csv
import matplotlib.pyplot as plt
import os
from PIL import Image

class Patient:
    def __init__(self):
        self.state = 0  # State 0 is healthy, state 1 is sick, state 2 is vaccinated
        self.healRate = 0
        self.infectRate = 0.2
        self.vacRate = 0.05

    def runPerc(self, rate):
        if random.random() < rate:
            return True
        else:
            return False

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

def update_grid():
    for x in range(rows):
        for y in range(columns):
            cells[x][y].configure(bg=get_color(mesh[x][y]))

def count_states():
    counts = {0: 0, 1: 0, 2: 0}
    for row in mesh:
        for patient in row:
            counts[patient.state] += 1
    return counts

def simulate(iteration=0):
    if iteration == 0:
        update_grid()  # Update the grid to display the initial state
        root.after(5000, simulate, iteration + 1)
    elif iteration < iterations:
        for x in range(rows):
            for y in range(columns):
                patient = mesh[x][y]
                if patient.state == 2:  # Vaccinated
                    pass
                elif patient.state == 0:  # Healthy
                    if iteration >= iterations // 2 and patient.runPerc(patient.vacRate):
                        patient.state = 2
                        patient.healRate = 1.0
                        patient.infectRate = 0
                elif patient.state == 1:  # Sick
                    if x != 0 and mesh[x - 1][y].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x - 1][y].state = 1
                    if x < rows - 1 and mesh[x + 1][y].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x + 1][y].state = 1
                    if y != 0 and mesh[x][y - 1].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x][y - 1].state = 1
                    if y < columns - 1 and mesh[x][y + 1].state == 0 and patient.runPerc(patient.infectRate):
                        mesh[x][y + 1].state = 1
                    if patient.runPerc(patient.healRate):
                        patient.state = 0
                        patient.healRate = 0
                        patient.infectRate = 0.3
                    else:
                        patient.healRate += 0.1
                        patient.infectRate -= 0.05

        update_grid()
        counts = count_states()
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

        # Save the image
        img.save(f'grids/grid_{iteration}.png')
        root.after(100, simulate, iteration + 1)
    else:
        data_file.close()


if __name__ == "__main__":
    os.makedirs('grids', exist_ok=True)
    root = tk.Tk()
    root.title("Disease Spread Simulation")

    rows, columns = 50, 50
    cell_size = 15
    mesh = [[Patient() for _ in range(columns)] for _ in range(rows)]
    cells = [[tk.Frame(root, bg="white", width=cell_size, height=cell_size) for _ in range(columns)] for _ in range(rows)]

    for x in range(rows):
        for y in range(columns):
            cells[x][y].grid(row=x, column=y)
            cells[x][y].pack_propagate(False)

    initialInfecPerc = 0.1
    initialInfec = int(rows * columns * initialInfecPerc)
    infected_cells = random.sample([(x, y) for x in range(rows) for y in range(columns)], initialInfec)
    for x, y in infected_cells:
        mesh[x][y].state = 1

    iterations = 150

    data_file = open('simulation_data.csv', 'w', newline='')
    data_writer = csv.writer(data_file)
    #data_writer.writerow(['Iteration', 'Healthy', 'Infected', 'Vaccinated'])

    # Write initial state (iteration 0) to CSV file
    initial_counts = count_states()
    data_writer.writerow([0, initial_counts[0], initial_counts[1], initial_counts[2]])

    simulate()  # Start the animation

    root.mainloop()

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

    # Plotting the results
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