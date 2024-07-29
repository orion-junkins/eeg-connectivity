import mne
import argparse
import os

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

    # Use MNE to guess the bads as a starting point
    # candidate_bads = mne.preprocessing.find_bad_channels_eeglab(raw)
    # Set the bad channels
    # raw.info['bads'] = candidate_bads  
    # TODO Explore if this is possible in MNE-Python

    # Plot the data and hang
    raw.plot(block=True)

    # Save the raw object to the same filepath
    raw.save(out_path, overwrite=True)

if __name__ == '__main__':
    # Call main handling args
    main()