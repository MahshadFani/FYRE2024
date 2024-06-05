import numpy as np
import matplotlib.pyplot as plt
import os

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    cell_bounds = {}
    atom_positions = []
    cell_lengths = {}

    for i, line in enumerate(lines):
        if "ITEM: ATOMS" in line:
            atom_data = lines[i + 1:]
            break
        elif "ITEM: BOX BOUNDS" in line:
            bounds_info = lines[i+1:i+4]
            for j, axis in enumerate(['x', 'y', 'z']):
                bounds = bounds_info[j].split()
                min_bound, max_bound = float(bounds[0]), float(bounds[1])
                cell_bounds[axis] = (min_bound, max_bound)
                cell_lengths[axis] = max_bound - min_bound

    atom_positions = np.array([[float(x) for x in line.split()[2:5]] for line in atom_data])
    return atom_positions, cell_bounds, cell_lengths

def calculate_fraction(atom_positions, cell_bounds, divisions):
    voxel_size = np.array([(cell_bounds[axis][1] - cell_bounds[axis][0]) / divisions for axis in ['x', 'y', 'z']])
    indices = np.floor((atom_positions - np.array([cell_bounds[axis][0] for axis in ['x', 'y', 'z']])) / voxel_size).astype(int)
    indices = np.clip(indices, 0, divisions - 1)

    grid = np.zeros((divisions, divisions, divisions), dtype=bool)
    grid[indices[:,0], indices[:,1], indices[:,2]] = True
    fraction = 1 - np.mean(grid)
    return fraction

def main():
    input_directory = '/scratch/mahshad1994/william.python/Cu1/10'
    output_directory = '/home/mahshad1994/Cu.containing.void/Cu1/10'
    output_file_path = os.path.join(output_directory, 'results.txt')
    divisions = 22
    initial_lengths = None
    results = []

    print("Checking output directory...")
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    print(f"Output directory: {output_directory}")

    print("Listing all files in the input directory...")
    # List all files in the directory (both files and directories)
    all_files = os.listdir(input_directory)
    print(f"All files in the input directory: {all_files}")

    # Filter only dump files
    dump_files = [f for f in all_files if f.startswith('dump.') and os.path.isfile(os.path.join(input_directory, f))]
    print(f"Dump files to process: {dump_files}")

    # Ensure 'dump.0' is processed first
    if 'dump.0' in dump_files:
        dump_files.remove('dump.0')
        dump_files.insert(0, 'dump.0')

    for file_name in dump_files:
        input_file_path = os.path.join(input_directory, file_name)
        print(f"Processing file: {input_file_path}")

        atom_positions, cell_bounds, cell_lengths = read_data(input_file_path)
        if initial_lengths is None:
            initial_lengths = cell_lengths

        px = (cell_lengths['x'] - initial_lengths['x']) / initial_lengths['x']
        py = (cell_lengths['y'] - initial_lengths['y']) / initial_lengths['y']
        pz = (cell_lengths['z'] - initial_lengths['z']) / initial_lengths['z']
        dilatation = -(px + py + pz) / 3.
        fraction = calculate_fraction(atom_positions, cell_bounds, divisions)
        results.append(f'{dilatation:.4f} {fraction:.4f}')
        print(f"Result for {file_name}: {dilatation:.4f} {fraction:.4f}")

    print(f"Writing results to {output_file_path}...")
    with open(output_file_path, 'w') as f:
        for result in results:
            f.write(result + '\n')

    print("Generating plot...")
    # Plotting and saving the figure instead of showing it
    plt.figure(figsize=(10, 5))
    plt.scatter([float(result.split()[0]) for result in results],
                [float(result.split()[1]) for result in results],
                color='blue')
    plt.title('Fraction vs. Dilatation')
    plt.xlabel('Dilatation')
    plt.ylabel('Fraction')
    plt.grid(True)
    plot_path = os.path.join(output_directory, 'plot.png')
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    main()
