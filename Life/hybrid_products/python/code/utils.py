# Johannes Zaeh, 26.05.2024
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource
from matplotlib.ticker import ScalarFormatter

'''
Function to read a txt-file of the form "attribute=value" to a dictionary.
'''


def read_input(path):
    input = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data = line.split("=")

            try:
                input[data[0]] = float(data[1])
            except:
                input[data[0]] = data[1]

    return input


'''
Function to write a dictionary to a txt-file like "key=value".
'''


def write_output(path, output):
    output_string = ""
    for key in output:
        if not isinstance(output[key], list):
            output_string += f"{key}={output[key]}\n"

    output_string += "\n\n\n"

    list_keys = []
    for key in output:
        if isinstance(output[key], list):
            list_keys.append(key)

    if len(list_keys) > 0:
        output_string += '\t'.join(list_keys)
        output_string += "\n"

        # Write rows
        for i in range(len(output[list_keys[0]])):
            row = '\t'.join(str(output[key][i]) for key in list_keys)
            output_string += row + '\n'

    with open(path, "w") as f:
        f.write(output_string)


'''
function to load fund data from a .txt file of the form mm/dd/yyyy[tab]value.
'''


def load_fund(path, start_date, duration):
    data = []
    with open(path, "r") as f:
        for j, line in enumerate(f):
            data.append(line.strip().replace(",", ".").split("\t"))
            data[j][1] = float(data[j][1])

    data = list(reversed(data))
    starting_index = 0
    for i, line in enumerate(data):
        if line[0] == start_date:
            starting_index = i

    fund = data[starting_index:starting_index + duration]
    for i in range(len(fund)):
        fund[i] = 1 + fund[i][1]

    return fund


'''
Load Life-Table
'''


def load_life_table(path):
    qx = []
    with open(path, "r") as f:
        for j, line in enumerate(f):
            qx.append(line.strip().replace(",", ".").split("\t")[1])
            qx[j] = float(qx[j])

    return qx


'''
2d Plot
'''


def twoD_plot(x, y):
    plt.close('all')
    # Apply a modern style
    plt.style.use('ggplot')

    # Create a plot
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(x, y, color='tab:blue', linewidth=2)

    # Customize labels
    ax.set_xlabel('Start Year', labelpad=15)
    ax.set_ylabel('Benefit at Maturity', labelpad=15)

    # Set the y-axis formatter to ScalarFormatter and disable offset and scientific notation
    formatter = ScalarFormatter(useOffset=False, useMathText=False)
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)

    # Optionally, set integer ticks for the y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Set the background color to transparent (optional)
    ax.patch.set_alpha(0.0)

    # Adjust tick parameters
    ax.tick_params(axis='both', which='major', labelsize=10, colors='gray')
    ax.tick_params(axis='both', which='minor', labelsize=8, colors='gray')

    # Remove grid lines
    ax.grid(False)

    # Set the background color for the axes to transparent (optional)
    # ax.set_facecolor((1.0, 1.0, 1.0, 0.0))
    # Display the plot
    plt.show()


'''
3d Plot
'''


def threeD_plot(x, y, z):
    plt.close('all')

    x, y = np.meshgrid(x, y)

    # Creating the 3D surface plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Apply a modern style ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    plt.style.use('ggplot')
    # color mapping (plasma,viridis,inferno,magma,coolwarm)
    cmap_id = 'viridis'

    # Create a surface plot with a modern colormap and edge colors
    surface = ax.plot_surface(x, y, z, cmap=cmap_id, edgecolor='none', antialiased=True, shade=True)

    # Add color bar for reference
    cbar = fig.colorbar(surface, ax=ax, shrink=0.3, aspect=10, format='%d')  # Format the color bar labels here
    cbar.set_label('Account Value')

    # Customize labels and remove the grid for a cleaner look
    ax.set_xlabel('Duration', labelpad=15)
    ax.set_ylabel('Start Year', labelpad=15)

    ax.set_zlabel('', labelpad=15)

    # Hide the z-axis pane
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Remove z-axis ticks
    ax.set_zticks([])

    # Set the background color to transparent (optional)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Adjust tick parameters
    ax.tick_params(axis='both', which='major', labelsize=10, colors='gray')
    ax.tick_params(axis='both', which='minor', labelsize=8, colors='gray')

    # Adjust the view angle for a better perspective
    ax.view_init(elev=30, azim=135)

    # Remove grid lines
    ax.grid(False)

    # Adjust the view angle for a better perspective
    ax.view_init(elev=30, azim=135)

    plt.show()
