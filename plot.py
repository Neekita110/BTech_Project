import os
import re
import matplotlib.pyplot as plt

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Initialize lists to store step, KE, and PE data
steps = []
ke = []
pe = []

# Correct path to the log file
log_file = 'C:/Users/hp/BTP/log.lammps'

try:
    # Open the log file and read the thermodynamic data
    with open(log_file, 'r') as f:
        in_thermo_section = False
        for line in f:
            # Look for the start of thermodynamic data
            if "Step Temp PotEng KinEng TotEng Press" in line:
                in_thermo_section = True
                continue
            # If in the thermo section and the line contains numeric data
            if in_thermo_section and re.match(r'^\s*\d+', line):
                cols = line.split()
                try:
                    steps.append(int(cols[0]))  # Step column
                    pe.append(float(cols[2]))   # Potential Energy column
                    ke.append(float(cols[3]))   # Kinetic Energy column
                except IndexError:
                    print(f"Skipping line due to missing data: {line}")
except FileNotFoundError as e:
    print(f"Error: {e}")

# Check if data was correctly extracted
if not steps:
    print("No data extracted from the log file. Please check the log format.")
else:
    # Plot KE and PE vs. Steps
    plt.figure(figsize=(10, 6))

    # Plot Potential Energy
    plt.subplot(2, 1, 1)
    plt.plot(steps, pe, label='Potential Energy (PE)', color='orange')
    plt.ylabel('Potential Energy')
    plt.legend()

    # Plot Kinetic Energy
    plt.subplot(2, 1, 2)
    plt.plot(steps, ke, label='Kinetic Energy (KE)', color='blue')
    plt.xlabel('Steps')
    plt.ylabel('Kinetic Energy')
    plt.legend()

    plt.tight_layout()
    plt.show()
