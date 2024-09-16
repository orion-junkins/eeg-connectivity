import mne 
import os
import numpy as np
from mne_connectivity import spectral_connectivity_time
import argparse
np.random.seed(42)
import sys

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Compute spectral connectivity metrics on processed EEG data")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('session', type=str, help='Session number')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", 
    help='Root directory of the data')
    parser.add_argument("--min_freq", help="Minimum frequency", default=0.5)
    parser.add_argument("--max_freq", help="Maximum frequency", default=12.0)
    parser.add_argument("--num_ica_comps", help="Number of ICA components", default=0.9999, type=float)
    parser.add_argument("--filter_string", help="Filter string to match annotations", required=True)
    parser.add_argument("--preserve_epochs", help="Whether to preserve epoch level precision or average across all", default="False", type=str)
    
    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    session = args.session
    min_freq = float(args.min_freq)
    max_freq = float(args.max_freq)
    num_ica_comps = args.num_ica_comps
    filter_string = args.filter_string
    avg_over_epochs = True if args.preserve_epochs.lower() == "false" else False

    # Define the input and output paths
    in_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_{num_ica_comps}_raw.fif')
    out_path = os.path.join(root_dir, 'connectivity_scores', expert, subject_id, f'{session}_{filter_string}_')
    
    # Make output dir
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Load the raw data
    raw = mne.io.read_raw_fif(in_path, preload=True)

    # Isolate the event of interest
    start_times = {
    }

    for annot in raw.annotations:
        start_times[annot["description"]] = annot["onset"]

    # Create a beg_keys sub list that includes only the start_times keys with the string "beg" somewhere inside
    beg_keys = [key for key in start_times.keys() if "beg" in key]

    # Filter beg_keys to only those that contain the expected string
    beg_keys = [key for key in beg_keys if filter_string in key]
    
    # Identify the corresponding end_keys for each beg_key by replacing "beg" with "end" and grabbing that key from start_times
    end_keys = [key.replace("beg", "end") for key in beg_keys]
    # Drop any end_keys that are not in start_times
    end_keys = [key for key in end_keys if key in start_times]

    # Create tuple pairs
    annotations_of_interest = list(zip(beg_keys, end_keys))

    print("annotations of interest: ", annotations_of_interest)
    assert(len(annotations_of_interest) > 0)
    epochs = []
    for pair in annotations_of_interest:
        start = start_times[pair[0]] + 2
        end = start_times[pair[1]] - 1
  
        raw_cropped = raw.copy().crop(tmin=start, tmax=end)

        # Isolate the frequency bands of interest
        # raw_delta = raw_cropped.copy().filter(l_freq=0.5, h_freq=4)

        # Split into epochs
        new_epochs = mne.make_fixed_length_epochs(raw_cropped, duration=5.0, overlap=2.5, preload=True)

        print(type(new_epochs))

        epochs.append(new_epochs)

        print(len(epochs))

    epochs = mne.epochs.concatenate_epochs(epochs)
   
    # Isolate the electrodes of interest: F3 (5),Fz (6),F4 (7),FCz (42),Cz (16),CP3 (48),CP4 (49),P1 (51),Pz (26),P2 (52),PPO1 (92) and PPO2 (93)
    channels_of_interest = ["F3", "Fz", "F4", "FCz", "Cz", "CP3", "CP4", "P1", "Pz", "P2", "PPO1", "PPO2"]
    indices_of_interest = [raw_cropped.ch_names.index(ch) for ch in channels_of_interest] # 0 indexed so 1 less than above
    epochs.pick(indices_of_interest)

    # Define the frequency intervals to study
    num_intervals = int((max_freq-min_freq) * 2) + 1
    freqs = np.linspace(min_freq, max_freq, num_intervals)
    n_cycles = freqs / 2.0

    # # Compute the spectral connectivity
    spec_con_obj = spectral_connectivity_time(epochs, freqs=freqs, method='plv', mode='multitaper', n_cycles=n_cycles, average=avg_over_epochs)
    arr = spec_con_obj.get_data(output="dense")

    # Store the connectivity array as a numpy array in the output path
    filename = "connectivity.npy" if avg_over_epochs else "epoch_connectivity.npy"
    np.save(out_path + filename, arr)

    print("Saved connectivity data to: ", out_path + filename)

    # # Save the channel names for reference
    np.save(out_path + 'channel_names.npy', channels_of_interest)

    # # Save the frequencies used for reference
    np.save(out_path + 'frequencies.npy', freqs)


if __name__ == '__main__':
    main()