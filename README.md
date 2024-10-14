# Calculations of Porosity 

## Foreword

This repository contains a Python script and a Jupyter Notebook for analyzing atomic position data from simulation output files. The script calculates the porosity of the material based on the space occupied by the atoms, analyzes the dilatation in the simulation cell, and visualizes the results. 


## Features

Data Reading: Recognizes atomic positions and cell boundaries from input files.

Calculation: Computes the fraction of the simulation cell occupied by atoms and the dilatation of the cell.

Output: Saves results to a text file of the porosity vs. dilatation.

The script is designed for the case where R = 0.772. To adapt the script for R = 2.316, the number of divisions should be changed from 21 to 63.

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



