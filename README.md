# Calculations of Void Fraction 

## Foreword

This repository contains a Python script and a Jupyter Notebook for analyzing atomic position data from simulation output files. The script calculates the fraction of the space occupied by atoms, analyzes the dilatation in the simulation cell, and visualizes the results. 


## Features

Data Reading: Parses atomic positions and cell boundaries from input files.

Calculation: Computes the fraction of the simulation cell occupied by atoms and the dilatation of the cell.

Output: Saves results to a text file of the void fraction vs. dilatation.
## Prerequisites
* Python 3.x
* NumPy
* Matplotlib

## Installation
Install the required Python packages:

pip install numpy matplotlib

## Usage
Running the Python Script:

Place your input files in the directory specified by input directory in the main() function. Ensure the output directory exists or will be created by the script.
Run the Script:

	python myscript.py



Results are saved to results.txt in the output directory.


Using the Jupyter Notebook:
Navigate to the repository directory and open myscript.ipynb.

## Example

To run the script, update the input directory and output directory variables in the main() function to your desired paths. The script will process the atomic data files, calculate the necessary values, and generate the output.



