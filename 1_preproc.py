import mne 
import numpy as np
import argparse
import os

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
    in_path = os.path.join(root_dir, 'raw', expert, subject_id, f'{session}_raw.fif')
    out_path = os.path.join(root_dir, 'preprocessed', expert, subject_id, f'{session}_raw.fif')
    ica_path = os.path.join(root_dir, 'ica', expert, subject_id, f'{session}_{num_ica_comps}_ica.fif')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(os.path.dirname(ica_path), exist_ok=True)

    # Load the raw data
    raw = mne.io.read_raw(f'{in_path}', preload=True)

    # Resample the data to 512Hz
    raw.resample(512)

    # Set the channel types for non-EEG channels
    channel_types = {
        'HEOGR': 'eog',
        'HEOGL': 'eog',
        'VEOGU': 'eog',
        'VEOGL': 'eog',
        'ECG': 'ecg',
        'M1': 'misc',
        'M2': 'misc',
    }
    raw.set_channel_types(channel_types)

    # Print what bad channels are being interpolated
    print(f'Interpolating bad channels: {raw.info["bads"]}')

    # Interpolate bad channels
    raw.interpolate_bads()

    # Set the reference to average and immediately apply the projection
    raw.set_eeg_reference('average', projection=True)
    raw.apply_proj()

    # Remove 50Hz line noise and harmonics
    raw.notch_filter([50, 100, 150, 200, 250], fir_design='firwin')

    # Apply bandpass filter for 0.5 to 40Hz
    raw.filter(0.5, 40, method='fir', fir_design='firwin')

    # Save the preprocessed data to a new file in MNE standard format
    raw.save(out_path, overwrite=True)

    # Initialize ICA object
    ica = mne.preprocessing.ICA(n_components=num_ica_comps, random_state=42)

    # Fit the ICA to the data
    ica.fit(raw)

    # Save the ICA object
    ica.save(ica_path, overwrite=True)

if __name__ == '__main__':
    main()