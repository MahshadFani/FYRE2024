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

def calculate_porosity(atom_positions, cell_bounds, divisions):
    voxel_size = np.array([(cell_bounds[axis][1] - cell_bounds[axis][0]) / divisions for axis in ['x', 'y', 'z']])
    indices = np.floor((atom_positions - np.array([cell_bounds[axis][0] for axis in ['x', 'y', 'z']])) / voxel_size).astype(int)
    indices = np.clip(indices, 0, divisions - 1)

    grid = np.zeros((divisions, divisions, divisions), dtype=bool)
    grid[indices[:,0], indices[:,1], indices[:,2]] = True
    porosity = 1 - np.mean(grid)
    return porosity

def main():
    input_directory = '/path/to/your/root'
    output_directory = '/path/to/your/root'
    output_file_path = os.path.join(output_directory, 'results.txt')
    divisions = 21
    initial_lengths = None
    results = []

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the directory (both files and directories)
    all_files = os.listdir(input_directory)

    # Filter only dump files
    dump_files = [f for f in all_files if f.startswith('dump.') and os.path.isfile(os.path.join(input_directory, f))]

    # Ensure 'dump.0' is processed first
    if 'dump.0' in dump_files:
        dump_files.remove('dump.0')
        dump_files.insert(0, 'dump.0')

    for file_name in dump_files:
        input_file_path = os.path.join(input_directory, file_name)
        atom_positions, cell_bounds, cell_lengths = read_data(input_file_path)
        if initial_lengths is None:
            initial_lengths = cell_lengths

        px = (cell_lengths['x'] - initial_lengths['x']) / initial_lengths['x']
        py = (cell_lengths['y'] - initial_lengths['y']) / initial_lengths['y']
        pz = (cell_lengths['z'] - initial_lengths['z']) / initial_lengths['z']
        dilatation = -(px + py + pz)
        porosity = calculate_porosity(atom_positions, cell_bounds, divisions)
        results.append(f'{file_name} {dilatation:.16f} {porosity:.4f}')

    with open(output_file_path, 'w') as f:
        for result in results:
            f.write(result + '\n')

    # Plotting and saving the figure instead of showing it
    plt.figure(figsize=(10, 5))
    dilatations = [float(result.split()[1]) for result in results]
    porosities = [float(result.split()[2]) for result in results]
    plt.scatter(dilatations, porosityies, color='blue')
    plt.title('porosity vs. Dilatation')
    plt.xlabel('Dilatation')
    plt.ylabel('porosity')
    plt.grid(True)
    plot_path = os.path.join(output_directory, 'plot.png')
    plt.savefig(plot_path)

if __name__ == "__main__":
    main()
