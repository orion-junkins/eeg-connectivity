import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_condition_diff_avg(group_a_condition_1, group_a_condition_2, group_b_condition_1, group_b_condition_2, dataset, title="Condition 2 - Condition 1"):
    group_a_diff = group_a_condition_2 - group_a_condition_1

    group_b_diff = group_b_condition_2 - group_b_condition_1

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


def plot_stacked_triple_ps(ps_groups, ps_conditions, ps_interactions, freqs, electrode_names, title="P Values", sub_title_1="Group", sub_title_2="Condition", sub_title_3="Interaction", save_path=None):
    fig, axs = plt.subplots(len(freqs), 3, figsize=(25, 8*len(freqs)))

    # Define a colormap that goes from bright yellow (at 0) to darker as it approaches 0.05
    cmap = plt.get_cmap('inferno_r')

    # Set vmin and vmax for the color scale (0.05 to 0)
    vmin, vmax = 0, 0.5

    # Helper function to annotate the cells with their values
    def annotate_heatmap(im, data):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if i <= j:
                    continue
                if data[i, j] > 0.1:
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
    