import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle
import mne
from mne.channels import make_standard_montage
import seaborn as sns

def plot_condition_diff_avg(group_a_condition_1, group_a_condition_2, group_b_condition_1, group_b_condition_2, dataset, title="Condition 1 - Condition 2"):
    group_a_diff =  group_a_condition_1 - group_a_condition_2

    group_b_diff = group_b_condition_1 - group_b_condition_2

    all_diffs = np.concatenate((group_a_diff, group_b_diff))

    all_diffs_avg = np.mean(all_diffs, axis=0)

    # Set a fixed vmin and vmax with large size
    sns.heatmap(all_diffs_avg, cmap="inferno_r", center=0, vmin=-0.025, vmax=0.025, annot=True, fmt=".3f", annot_kws={"fontsize": 8})

    # Set the figure size
    plt.gcf().set_size_inches(10, 10)

    # Use dataset.electrode_names for the ticklabels, shifting slightly to be centered in each col
    plt.xticks(np.arange(len(dataset.electrode_names)), dataset.electrode_names, rotation=0, fontsize=8, ha="left")
    plt.yticks(np.arange(len(dataset.electrode_names)), dataset.electrode_names, rotation=0, fontsize=8, va="top")
    
    plt.title(title)
    plt.show()


def plot_condition_diff_avg_2way(group_a_condition_1, group_a_condition_2, dataset, title="Condition 1 - Condition 2"):
    all_diffs =  group_a_condition_1 - group_a_condition_2

    all_diffs_avg = np.mean(all_diffs, axis=0)

    # Set a fixed vmin and vmax with large size
    sns.heatmap(all_diffs_avg, cmap="inferno_r", center=0, vmin=-0.025, vmax=0.025, annot=True, fmt=".3f", annot_kws={"fontsize": 8})

    # Set the figure size
    plt.gcf().set_size_inches(10, 10)

    # Use dataset.electrode_names for the ticklabels, shifting slightly to be centered in each col
    plt.xticks(np.arange(len(dataset.electrode_names)), dataset.electrode_names, rotation=0, fontsize=8, ha="left")
    plt.yticks(np.arange(len(dataset.electrode_names)), dataset.electrode_names, rotation=0, fontsize=8, va="top")
    
    plt.title(title)
    plt.show()


def plot_single_p_value_table(np_array, electrode_names, title="P Values"):
    # Define a colormap that goes from bright yellow (at 0) to darker as it approaches 0.05
    cmap = plt.get_cmap('inferno_r')

    # Set vmin and vmax for the color scale (0.05 to 0)
    vmin, vmax = 0, 0.5

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(np_array, cmap=cmap, vmin=vmin, vmax=vmax, ax=ax)

    # Annotate heatmap
    for i in range(12):
        for j in range(12):
            if i <= j:
                continue
            if np_array[i, j] > 0.1:
                continue
            ax.text(j + 0.5, i + 0.5, f'{np_array[i, j]:.2f}', ha='center', va='center', color='black')
    
    ax.set_xticklabels(electrode_names, rotation=45)
    ax.set_yticklabels(electrode_names, rotation=0)
    ax.set_title(title)
    
    plt.show()


def plot_heatmap(np_array, electrode_names, title, vmin=None, vmax=None, print_min=None, print_max=None, lower_triangular_only=True):
    if vmin is None:
        vmin = np.min(np_array)
    if vmax is None:
        vmax = np.max(np_array)
    if print_min is None:
        print_min = np.min(np_array)
    if print_max is None:
        print_max = np.max(np_array)
    # Define a colormap that goes from bright yellow (at 0) to darker as it approaches 0.05
    cmap = plt.get_cmap('inferno_r')

    fig, ax = plt.subplots(figsize=(10, 8))
    if lower_triangular_only:
        data = np.tril(np_array)
    else:
        data = np_array
    
    sns.heatmap(data, cmap=cmap, vmin=vmin, vmax=vmax, ax=ax)

    # Annotate heatmap
    for i in range(12):
        for j in range(12):
            if lower_triangular_only and i <= j:
                continue
            if data[i, j] >= print_min and data[i, j] <= print_max:
                ax.text(j + 0.5, i + 0.5, f'{data[i, j]:.3f}', ha='center', va='center', color='black', fontsize=8)
    
    ax.set_xticklabels(electrode_names, rotation=45)
    ax.set_yticklabels(electrode_names, rotation=0)
    ax.set_title(title)

    plt.show()


def plot_triple_p_value_table(ps_group, ps_condition, ps_interaction, electrode_names, title="P Values", sub_title_1="Group", sub_title_2="Condition", sub_title_3="Interaction"):
    fig, axs = plt.subplots(1, 3, figsize=(25, 10), )

    # Define a colormap that goes from bright yellow (at 0) to darker as it approaches 0.05
    cmap = plt.get_cmap('inferno_r')

    # Set vmin and vmax for the color scale (0.05 to 0)
    vmin, vmax = 0, 0.5

    # Helper function to annotate the cells with their values
    def annotate_heatmap(im, data):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if data[i, j] > 0.1:
                    continue
                if np.isnan(data[i, j]):
                    continue
                text = im.axes.text(j, i, f"{data[i, j]:.2f}",
                                    ha="center", va="center", color="black")

    # Group p values
    im0 = axs[0].imshow(ps_group[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
    annotate_heatmap(im0, ps_group[:, :])
    axs[0].set_title(sub_title_1, fontsize=20)

    # Condition p values
    im1 = axs[1].imshow(ps_condition[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
    annotate_heatmap(im1, ps_condition[:, :])
    axs[1].set_title(sub_title_2, fontsize=20)

    # Interaction p values
    im2 = axs[2].imshow(ps_interaction[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
    annotate_heatmap(im2, ps_interaction[:, :])
    axs[2].set_title(sub_title_3, fontsize=20)

    # Create a single color bar that spans all subplots
    fig.colorbar(im0, ax=axs, orientation='vertical', fraction=0.02, pad=0.04)

    # Set the x and y labels
    for ax in axs:
        ax.set_xticks(range(len(electrode_names)))
        ax.set_xticklabels(electrode_names, rotation=90)
        ax.set_yticks(range(len(electrode_names)))
        ax.set_yticklabels(electrode_names)

    # Set the overall title
    fig.suptitle(title, fontsize=30)

    plt.show()


def plot_stacked_triple_ps(ps_groups, ps_conditions, ps_interactions, freqs, electrode_names, title="P Values", sub_title_1="Group", sub_title_2="Condition", sub_title_3="Interaction", save_path=None, vmin=0, vmax=0.5, cutoff=0.1):
    fig, axs = plt.subplots(len(freqs), 3, figsize=(25, 8*len(freqs)))

    # Define a colormap that goes from bright yellow (at 0) to darker as it approaches 0.05
    cmap = plt.get_cmap('inferno_r')

    # Helper function to annotate the cells with their values
    def annotate_heatmap(im, data):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if i <= j:
                    continue
                if data[i, j] > cutoff:
                    continue
                if np.isnan(data[i, j]):
                    continue
                text = im.axes.text(j, i, f"{data[i, j]:.2g}",
                                    ha="center", va="center", color="black")

    for i, (ps_group, ps_condition, ps_interaction) in enumerate(zip(ps_groups, ps_conditions, ps_interactions)):
        # Group p values
        im0 = axs[i, 0].imshow(ps_group[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
        annotate_heatmap(im0, ps_group[:, :])
        axs[i, 0].set_title(sub_title_1 + " - " + str(freqs[i]), fontsize=20)
        
        # Condition p values
        im1 = axs[i, 1].imshow(ps_condition[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
        annotate_heatmap(im1, ps_condition[:, :])
        axs[i, 1].set_title(sub_title_2  + " - " + str(freqs[i]), fontsize=20)

        # Interaction p values
        im2 = axs[i, 2].imshow(ps_interaction[:, :], cmap=cmap, vmin=vmin, vmax=vmax)
        annotate_heatmap(im2, ps_interaction[:, :])
        axs[i, 2].set_title(sub_title_3  + " - " + str(freqs[i]), fontsize=20)

        # Create a single color bar that spans all subplots
        fig.colorbar(im0, ax=axs[i, :], orientation='vertical', fraction=0.02, pad=0.04)

        # Set the x and y labels
        for ax in axs[i, :]:
            ax.set_xticks(range(len(electrode_names)))
            ax.set_xticklabels(electrode_names, rotation=90)
            ax.set_yticks(range(len(electrode_names)))
            ax.set_yticklabels(electrode_names)
        
    # Set the overall title
    fig.suptitle(title, fontsize=50)
    
    # Add a subtitle listing frequency bands from freqs
    fig.text(0.5, 0.92, 'Frequency Bands: ' + ', '.join([str(freq) for freq in freqs]), ha='center', fontsize=20)

    if save_path:
        plt.savefig(save_path)
    plt.show()
    

def plot_connectivity(connections, save_path=None,
                        electrodes_of_interest=["F3", "Fz", "F4", "FCz", "Cz", "CP3", "CP4", "P1", "Pz", "P2", "PPO1", "PPO2"], montage_viz_path="data/montage_viz_pos.npz"):
    all_positions_loaded = np.load(montage_viz_path)
    all_positions = {key: all_positions_loaded[key] for key in all_positions_loaded}

    # Define a projection function for 3D to 2D
    def azimuthal_equidistant_projection(pos):
        x, y, z = pos
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        return r * np.cos(theta), r * np.sin(theta)

    # Projection all electrode positions to 2D
    all_positions = {name: azimuthal_equidistant_projection(coord) for name, coord in all_positions.items()}
    print(all_positions)

    # Scale and shift positions to align nicely with head diagram
    scaling_factor = 7
    all_positions = {name: (coord[0] * scaling_factor, coord[1] * scaling_factor) for name, coord in all_positions.items()}
    all_positions = {name: (coord[0], coord[1] + 0.08) for name, coord in all_positions.items()}

    # Extract 2D positions for the electrodes of interest
    primary_positions = {name: all_positions[name] for name in electrodes_of_interest}

    # Create our base figure
    fig, ax = plt.subplots(figsize=(16, 16))

    # Plot connections between electrodes
    for connection in connections:
        e1_name = connection[0]
        e2_name = connection[1]
        start = primary_positions[e1_name]
        end = primary_positions[e2_name]

        # Check if the connection is Pz to Fz and draw a slight arc instead of a line (avoids ambiguity)
        if e1_name == "Pz" and e2_name == "Fz" or e1_name == "Fz" and e2_name == "Pz":
            center_x = (start[0] + end[0]) / 2
            center_y = (start[1] + end[1]) / 2
            arc = Arc(
                (center_x + 0.167, center_y),
                1.7,              
                0.44,            
                angle=90,                
                theta1=20,              
                theta2=160,            
                color='black',
                lw=2 
            )
            ax.add_patch(arc)       
        else:
            ax.plot([start[0], end[0]], [start[1], end[1]], c='black', lw=2)

    # Plot all electrodes as gray circles
    for coord in all_positions.values():
        circle = Circle(coord, 0.02, color='gray', fill=True)
        ax.add_patch(circle)

    # Highlight electrodes of interest as black circles with labels inside
    for name, coord in primary_positions.items():
        circle = Circle(coord, 0.03, color='black', fill=True) 
        ax.add_patch(circle)
        ax.text(coord[0], coord[1], name, color='white', ha='center', va='center', fontsize=10) 

    # Add a head + nose
    circle = plt.Circle((0, 0), 0.8, color='black', fill=False, lw=2) 
    ax.add_artist(circle)
    nose_x = [-0.1, 0, 0.1]
    nose_y = [0.8, 0.9, 0.8]
    ax.plot(nose_x, nose_y, color='black', lw=2)

    # Plot the figure
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    plt.show()

    if save_path:
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0)


def dict_to_latex_table(data, col_width="3cm"):
    # Check that all columns have the same number of rows
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All list values in the dictionary must have the same length.")
    
    # Prepare headers and rows
    headers = list(data.keys())
    rows = zip(*data.values())
    
    # Build the column format (e.g., "|c|c|c|")
    col_format = "|" + "|".join([f"p{{{col_width}}}" for _ in headers]) + "|"
    
    # Build the LaTeX code
    latex_str = []
    latex_str.append("\\begin{table}[h!]")
    latex_str.append("  \\small")
    latex_str.append("  \\centering")
    latex_str.append("  \\caption{Table X: Description...}")
    latex_str.append("  \\begin{tabular}{" + col_format + "}")
    latex_str.append("    \\hline")
    
    # Add header row
    latex_str.append("    " + " & ".join(headers) + " \\\\ \\hline")
    
    # Add data rows
    for row in rows:
        row_str = " & ".join(str(x) for x in row)
        latex_str.append("    " + row_str + " \\\\ ")
    latex_str.append("    \\hline")
    latex_str.append("  \\end{tabular}")
    latex_str.append("\\end{table}")
    
    return "\n".join(latex_str)
