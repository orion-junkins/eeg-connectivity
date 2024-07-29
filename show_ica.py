import mne 
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

np.random.seed(42)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Preprocess EEG data with MNE")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('session', type=str, help='Session number')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", help='Root directory of the data')
    parser.add_argument("--num_ica_comps", help="Number of ICA components", default=20, type=int)

    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    session = args.session
    num_ica_comps = args.num_ica_comps

    # Define input and output paths
    in_path = os.path.join(root_dir, 'preprocessed', expert, subject_id, f'{session}_raw.fif')
    out_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_raw.fif')
    ica_path = os.path.join(root_dir, 'ica', expert, subject_id, f'{session}_{num_ica_comps}_ica.fif')

    # Load the raw and ica data
    raw = mne.io.read_raw_fif(in_path, preload=True)
    ica = mne.preprocessing.read_ica(ica_path)

    # Plot ICA component topologies
    ica.plot_components(inst=raw)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()