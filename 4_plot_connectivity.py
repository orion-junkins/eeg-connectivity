import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import argparse
np.random.seed(42)


def plot_connectivity(data, channel_names, freqs, title):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    t = 0
    l = plt.imshow(data[:, :, t], cmap='viridis', aspect='auto')
    axcolor = 'lightgoldenrodyellow'
    axtime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    stime = Slider(axtime, 'Frequency', freqs[0], freqs[-1], valinit=freqs[t], valstep=freqs[1]-freqs[0])

    # Update the image when the slider is moved
    def update(val):
        freq = stime.val
        t = np.argmin(np.abs(freqs - freq))
        l.set_data(data[:, :, t])
        fig.canvas.draw_idle()
    stime.on_changed(update)

    # Set labels as the electrode names
    ax.set_xticks(np.arange(len(channel_names)))
    ax.set_yticks(np.arange(len(channel_names)))
    ax.set_xticklabels(channel_names)
    ax.set_yticklabels(channel_names)

    # Add a colorbar
    plt.colorbar(l)

    # Add title
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Show the plot in an interactive window
    plt.show()


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Plot spectral connectivity metrics on processed EEG data")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('session', type=str, help='Session number')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", 
    help='Root directory of the data')

    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    session = args.session

    # Load data
    dir = os.path.join(root_dir, "connectivity_scores", expert, subject_id)
    connectivity = np.load(os.path.join(dir, f'{session}_connectivity.npy'))
    frequencies = np.load(os.path.join(dir, f'{session}_frequencies.npy'))
    channel_names = np.load(os.path.join(dir, f'{session}_channel_names.npy'))
    
    # Render Plot
    plot_connectivity(connectivity, channel_names, frequencies, title=f'{expert} {subject_id}: session {session}')


if __name__ == "__main__":
    main()