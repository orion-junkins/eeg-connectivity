import mne 
import os
import numpy as np
import argparse

np.random.seed(42)
import numpy as np

import numpy as np
from scipy.signal import hilbert
from itertools import combinations

def phase_synchrony_via_normalized_entropy(epochs):
    """
    Calculates pairwise phase synchrony indices based on entropy of phase difference distribution for each epoch.

    Args:
        epochs: MNE Epochs object containing the EEG data.
    
    Returns:
        synchrony_matrices : ndarray, shape (n_epochs, n_channels, n_channels)
        Array of synchronization indices for each epoch.
    """
    # Define the number of bins in the phase difference distribution
    BINS = 50  

    # Extract data from epochs with shape (n_epochs, n_channels, n_times)
    data = epochs.get_data(copy=False) 
    n_epochs, n_channels, n_times = data.shape

    # Initialize the synchrony matrix for all epochs
    synchrony_matrices = np.zeros((n_epochs, n_channels, n_channels))

    # Generate all unique pairs of channels
    pairs = np.array(list(combinations(range(n_channels), 2)))  # Shape: (n_pairs, 2)
    n_pairs = pairs.shape[0]

    # Loop over epochs
    for epoch_idx in range(n_epochs):
        epoch_data = data[epoch_idx, :, :]  # Shape: (n_channels, n_times)

        # Initialize the synchronization indices matrix for this epoch
        s = np.zeros((n_channels, n_channels))

        # Transpose to flip shape
        epoch_data_T = epoch_data.T  # Shape: (n_times, n_channels)

        # Compute the analytic signal using the Hilbert transform
        analytic_signal = hilbert(epoch_data_T, axis=0)

        # Extract the instantaneous phase
        ph = np.angle(analytic_signal)  # Shape: (n_times, n_channels)

        # Compute the phase difference for all pairs of electrodes
        ph1 = ph[:, pairs[:, 0]]  # Shape: (n_times, n_pairs)
        ph2 = ph[:, pairs[:, 1]]  # Shape: (n_times, n_pairs)
        phdiff = ph1 - ph2  # Shape: (n_times, n_pairs)

        # Wrap phase differences to the range [-pi, pi] (MATLAB does this automatically)
        phdiff = np.angle(np.exp(1j * phdiff))

        # Bin the phase differences into B bins over the range [−pi, pi] to form a histogram
        bin_edges = np.linspace(-np.pi, np.pi, BINS + 1)
        bin_indices = np.digitize(phdiff, bins=bin_edges) - 1 
        counts = np.zeros((BINS, n_pairs))
        for i in range(n_pairs):
            indices = bin_indices[:, i]
            counts[:, i] = np.bincount(indices, minlength=BINS)

        # Normalize histograms to get probability distributions
        d = counts / (np.sum(counts, axis=0, keepdims=True) + np.finfo(float).eps)

        # Compute the entropy
        logd = np.log(d + np.finfo(float).eps)
        h = np.sum(d * logd, axis=0) / np.log(BINS)

        # Fill the synchrony matrix with the computed entropy values
        for idx, (k, m) in enumerate(pairs):
            s[k, m] = h[idx]
            s[m, k] = h[idx]

        # Store the synchronization matrix for this epoch
        synchrony_matrices[epoch_idx, :, :] = s

    return synchrony_matrices

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Compute spectral connectivity metrics on processed EEG data")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", 
    help='Root directory of the data')
    parser.add_argument("--num_ica_comps", help="Number of ICA components", default=0.9999, type=float)
    parser.add_argument("--dir_suffix", help="Suffix for the directory", default="", type=str)
    parser.add_argument("--baseline", help="Whether to use baseline data", default="False", type=str)
    parser.add_argument("--WiG", help="Whether to use data with or without gestures", default="False", type=str)
    parser.add_argument("--epoch_duration", help="Duration of each epoch in seconds", default=5.0, type=float)
    parser.add_argument("--epoch_overlap", help="Overlap between epochs in seconds", default=2.5, type=float)
    
    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    num_ica_comps = args.num_ica_comps
    dir_suffix = args.dir_suffix
    epoch_duration = args.epoch_duration
    epoch_overlap = args.epoch_overlap

    baseline = True if args.baseline.lower() == "true" else False
    with_gestures = True if args.WiG.lower() == "true" else False

    # Define output path
    out_filename_prefix = ""
    if baseline:
        out_filename_prefix += "BL_"
    if with_gestures:
        out_filename_prefix += "WiG_"
    else:
        out_filename_prefix += "NoG_"
    
    out_path = os.path.join(root_dir, 'connectivity_scores' + dir_suffix, expert, subject_id, out_filename_prefix + "connectivity.npy")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    frequency_bands = [(0.5,4.0), (4.0,8.0), (8.0,10.0), (10.0,13.0), (13.0,20.0), (20.0,30.0)]
    all_connectivity = []

    for band in frequency_bands:
        # Compile a single list of epochs across all sessions
        epochs = []

        for session in range(1, 5):
            # Load the raw data
            in_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_{num_ica_comps}_raw.fif')            
            try:
                raw = mne.io.read_raw_fif(in_path, preload=True)
            except FileNotFoundError:
                print("Skipping session ", session, " due to missing file")
                continue
            
            # Filter to the current frequency band
            lower_bound = band[0]
            upper_bound = band[1]
            raw = raw.filter(l_freq=lower_bound, h_freq=upper_bound)

            # Isolate the events of interest
            start_times = {}
            for annot in raw.annotations:
                start_times[annot["description"]] = annot["onset"]

            # Create a beg_keys sub list that includes only the start_times keys with the string "beg" somewhere inside
            beg_keys = [key for key in start_times.keys() if "beg" in key]
            # Isolate only the events corresponding to the correct gesture/no gesture condition
            filter_string = "WiG" if with_gestures else "NoG"
            beg_keys = [key for key in beg_keys if filter_string in key]
            
            # Isolate only the events corresponding to the correct baseline/no baseline condition
            if baseline:
                # Remove keys missing "BL"
                beg_keys = [key for key in beg_keys if "BL" in key]
            else:
                # Remove keys containing "BL"
                beg_keys = [key for key in beg_keys if "BL" not in key]

            # Identify the corresponding end_keys for each beg_key by replacing "beg" with "end" and grabbing that key from start_times
            end_keys = [key.replace("beg", "end") for key in beg_keys]
            # Drop any end_keys that are not in start_times
            end_keys = [key for key in end_keys if key in start_times]
            # Create tuple pairs
            annotations_of_interest = list(zip(beg_keys, end_keys))
            print("annotations of interest: ", annotations_of_interest) 

            # Proceed to the next session if no annotations of interest were found
            if len(annotations_of_interest) == 0:
                continue

            # Create epochs for each pair of annotations and add them to the global list of all epochs
            for pair in annotations_of_interest:
                # Ignore the first two seconds and the last second of event
                start = start_times[pair[0]] + 2
                end = start_times[pair[1]] - 1
                raw_cropped = raw.copy().crop(tmin=start, tmax=end)

                # Make epochs
                new_epochs = mne.make_fixed_length_epochs(raw_cropped, duration=epoch_duration, overlap=epoch_overlap, preload=True)

                # Append the new epochs to the global list
                epochs.append(new_epochs)

        if len(epochs) == 0:
            print("No epochs found for frequency band ", band)
            continue
        epochs = mne.epochs.concatenate_epochs(epochs)

        # Isolate the electrodes of interest: F3 (5),Fz (6),F4 (7),FCz (42),Cz (16),CP3 (48),CP4 (49),P1 (51),Pz (26),P2 (52),PPO1 (92) and PPO2 (93)
        electrodes_of_interest = ["F3", "Fz", "F4", "FCz", "Cz", "CP3", "CP4", "P1", "Pz", "P2", "PPO1", "PPO2"]
        indices_of_interest = [raw.ch_names.index(ch) for ch in electrodes_of_interest] # 0 indexed so 1 less than above
        epochs.pick(indices_of_interest)

        connectivity = phase_synchrony_via_normalized_entropy(epochs)
        all_connectivity.append(connectivity)
    
    all_connectivity_arr = np.stack(all_connectivity, axis=3)

    np.save(out_path, all_connectivity_arr)
    print("Saved connectivity data to: ", out_path)

if __name__ == '__main__':
    main()