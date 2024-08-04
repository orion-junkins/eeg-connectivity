import mne
import argparse
import os
import numpy as np

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Mark bad channels in EEG data interactively")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the subject')
    parser.add_argument('session', type=str, help='Session identifier')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg/", help='Root directory of the data')

    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    session = args.session

    # Define data input and output path
    in_path = os.path.join(root_dir, 'raw', expert, subject_id, f'{session}.set')
    out_path = os.path.join(root_dir, 'raw', expert, subject_id, f'{session}_raw.fif')

    # Load the EEG data
    raw = mne.io.read_raw_eeglab(in_path, preload=True)

    # Calculate the standard deviation of each channel
    data = raw.get_data()
    std_devs = np.std(data, axis=1)

    # Calculate the median and a threshold for detecting bad channels
    median_std = np.median(std_devs)
    max_std = 50 
    min_std = 0.00001

    # Find channels with standard deviations significantly above the median
    candidate_bads = [raw.ch_names[i] for i, std in enumerate(std_devs) if std > max_std * median_std or std < min_std]
    print("Automatic candidate_bads: " + str(candidate_bads))

    # Set the candidates as the initial guess for bad channels
    raw.info['bads'] = candidate_bads

    # Plot the data and hang to allow user to finalize selections
    raw.plot(block=True)

    # Print the final list of bad channels
    print("Final bads: " + str(raw.info['bads']))

    # Save the raw object to the same filepath
    raw.save(out_path, overwrite=True)

if __name__ == '__main__':
    # Call main handling args
    main()