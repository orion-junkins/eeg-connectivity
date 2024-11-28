import numpy as np
import matplotlib.pyplot as plt

def plot_all_diffs(diff_groups, diff_conditions, freqs, channel_names, title="Mean Differences", sub_title_1="Group Mean Difference", sub_title_2="Condition Mean Difference", save_path=None):
    num_freqs = len(freqs)
    fig, axs = plt.subplots(num_freqs, 2, figsize=(20, 8 * num_freqs))

    # Ensure axs is a 2D array even if num_freqs == 1
    if num_freqs == 1:
        axs = np.array([axs])

    # Choose a diverging colormap centered at zero
    cmap = plt.get_cmap('seismic')  # Options: 'seismic', 'bwr', 'coolwarm'

    # Helper function to annotate the heatmaps
    def annotate_heatmap(im, data, valfmt="{x:.3f}", **textkw):
        kw = dict(horizontalalignment="center", verticalalignment="center")
        kw.update(textkw)

        # Loop over the data and create a text annotation for each cell
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if i <= j:
                    continue
                value = data[i, j]
                if np.isnan(value):
                    continue
                text = im.axes.text(j, i, valfmt.format(x=value), **kw)

    for i, (diff_group, diff_condition) in enumerate(zip(diff_groups, diff_conditions)):
        # Determine vmin and vmax for each subplot based on the data
        max_abs_value_group = np.nanmax(np.abs(diff_group))
        vmin_group = -0.3
        vmax_group = 0.3

        max_abs_value_condition = np.nanmax(np.abs(diff_condition))
        vmin_condition = -0.3
        vmax_condition = 0.3

        # Plot Group Mean Differences
        im0 = axs[i, 0].imshow(diff_group, cmap=cmap, vmin=vmin_group, vmax=vmax_group)
        annotate_heatmap(im0, diff_group)
        axs[i, 0].set_title(f"{sub_title_1} ({freqs[i]})", fontsize=20)

        # Plot Condition Mean Differences
        im1 = axs[i, 1].imshow(diff_condition, cmap=cmap, vmin=vmin_condition, vmax=vmax_condition)
        annotate_heatmap(im1, diff_condition)
        axs[i, 1].set_title(f"{sub_title_2} ({freqs[i]})", fontsize=20)

        # Add colorbars for each subplot
        cbar0 = fig.colorbar(im0, ax=axs[i, 0], orientation='vertical', fraction=0.046, pad=0.04)
        cbar1 = fig.colorbar(im1, ax=axs[i, 1], orientation='vertical', fraction=0.046, pad=0.04)

        # Set x and y labels
        for ax in axs[i, :]:
            ax.set_xticks(range(len(channel_names)))
            ax.set_xticklabels(channel_names, rotation=90)
            ax.set_yticks(range(len(channel_names)))
            ax.set_yticklabels(channel_names)

    # Set the overall title
    fig.suptitle(title, fontsize=50, y=1.02)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    plt.show()

import seaborn as sns

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


    