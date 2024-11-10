import mne 
import os
import numpy as np
from mne_connectivity import spectral_connectivity_time
import argparse

np.random.seed(42)
import numpy as np

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Compute spectral connectivity metrics on processed EEG data")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", 
    help='Root directory of the data')
    parser.add_argument("--min_freq", help="Minimum frequency", default=0.5)
    parser.add_argument("--max_freq", help="Maximum frequency", default=30.0)
    parser.add_argument("--num_ica_comps", help="Number of ICA components", default=0.9999, type=float)
    parser.add_argument("--dir_suffix", help="Suffix for the directory", default="", type=str)
    parser.add_argument("--PLV_method", help="PLV Method for MNE", default="pli", type=str)
    parser.add_argument("--n_cycles_numerator", help="Numerator for the number of cycles", default=2, type=int)
    parser.add_argument("--baseline", help="Whether to use baseline data", default="False", type=str)
    parser.add_argument("--WiG", help="Whether to use data with or without gestures", default="False", type=str)
    
    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    min_freq = float(args.min_freq)
    max_freq = float(args.max_freq)
    num_ica_comps = args.num_ica_comps
    dir_suffix = args.dir_suffix
    plv_method = args.PLV_method
    n_cycles_numerator = args.n_cycles_numerator

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
    frequency_filepath = os.path.join(root_dir, 'connectivity_scores', expert, subject_id, 'frequencies.npy')
    channel_names_filepath = os.path.join(root_dir, 'connectivity_scores', expert, subject_id, 'channel_names.npy')

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Compile a single list of epochs across all sessions
    epochs = []
    for session in range(1, 5):
        previous_epoch_count = len(epochs)
        print("Processing session ", session)

        in_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_{num_ica_comps}_raw.fif')

        # Load the raw data
        try:
            raw = mne.io.read_raw_fif(in_path, preload=True)
        except FileNotFoundError:
            print("Skipping session ", session, " due to missing file")
            continue
        
        # Isolate the events of interest
        start_times = {
        }

        for annot in raw.annotations:
            start_times[annot["description"]] = annot["onset"]

        # Create a beg_keys sub list that includes only the start_times keys with the string "beg" somewhere inside
        beg_keys = [key for key in start_times.keys() if "beg" in key]

        # Filter beg_keys to only those that contain the expected string
        filter_string = "WiG" if with_gestures else "NoG"
        beg_keys = [key for key in beg_keys if filter_string in key]

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
        if len(annotations_of_interest) == 0:
            print("No annotations of interest found for session ", session)
            continue
        else: 
            print("Found annotations of interest for session ", session)
            print(annotations_of_interest)
        
        for pair in annotations_of_interest:
            start = start_times[pair[0]] + 2
            end = start_times[pair[1]] - 1
            raw_cropped = raw.copy().crop(tmin=start, tmax=end)

            new_epochs = mne.make_fixed_length_epochs(raw_cropped, duration=5.0, overlap=2.5, preload=True)

            epochs.append(new_epochs)

        print("Added ", len(epochs) - previous_epoch_count, " epochs to the list")

        epochs = mne.epochs.concatenate_epochs(epochs)

    if len(epochs) == 0:
        print("No epochs found for subject ", subject_id)
        return
    

    # Isolate the electrodes of interest: F3 (5),Fz (6),F4 (7),FCz (42),Cz (16),CP3 (48),CP4 (49),P1 (51),Pz (26),P2 (52),PPO1 (92) and PPO2 (93)
    channels_of_interest = ["F3", "Fz", "F4", "FCz", "Cz", "CP3", "CP4", "P1", "Pz", "P2", "PPO1", "PPO2"]
    indices_of_interest = [raw_cropped.ch_names.index(ch) for ch in channels_of_interest] # 0 indexed so 1 less than above
    epochs.pick(indices_of_interest)

    # Define the frequency intervals to study
    num_intervals = int((max_freq-min_freq) * 2) + 1
    freqs = np.linspace(min_freq, max_freq, num_intervals)
    n_cycles = freqs / n_cycles_numerator

    # Compute the spectral connectivity
    spec_con_obj = spectral_connectivity_time(epochs, freqs=freqs, method=plv_method, mode='multitaper', n_cycles=n_cycles, average=False)
    arr = spec_con_obj.get_data(output="dense")

    # Check if a channel_names file exists. If it does, verify that it is the same as the current channels_of_interest. If it is not the same, throw an exception
    if os.path.exists(channel_names_filepath):
        saved_channels = np.load(channel_names_filepath)
        if not np.array_equal(saved_channels, channels_of_interest):
            raise Exception("Channel names do not match the saved channel names")
    else:
        # Save the channel names
        np.save(channel_names_filepath, channels_of_interest)

    # Same for frequencies
    if os.path.exists(frequency_filepath):
        saved_freqs = np.load(frequency_filepath)
        if not np.array_equal(saved_freqs, freqs):
            raise Exception("Frequencies do not match the saved frequencies")
    else:
        # Save the frequencies
        np.save(frequency_filepath, freqs)

    # Store the connectivity array as a numpy array in the output path
    np.save(out_path, arr)
    print("Saved connectivity data to: ", out_path)

if __name__ == '__main__':
    main()