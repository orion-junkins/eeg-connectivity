import mne 
import numpy as np
import argparse
from data.bad_channels import bad_channels

np.random.seed(42)

# Read command line argument for expert or novice, id and session
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="'expert' or 'novice'")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
args = parser.parse_args()

# Define the input and output paths
in_path = f'data/raw/{args.expert}_{args.id}_{args.session}.set'
out_path = f'data/processed/{args.expert}_{args.id}_{args.session}_raw.fif'

# Load the .set and .fdt files
raw = mne.io.read_raw_eeglab(in_path, preload=True)

# Resample the data to 512Hz
raw.resample(512)

# Set the channel types for non-EEG channels
channel_types = {
    'HEOGR': 'eog',
    'HEOGL': 'eog',
    'VEOGU': 'eog',
    'VEOGL': 'eog',
    'M1': 'misc',  # Set M1 as misc
    'M2': 'misc',   # Set M2 as misc
    "OI2h": "ecg",
    "OI2h": "ecg",
}
raw.set_channel_types(channel_types)

# Interpolate bad channels
raw.info['bads'] = bad_channels[f'{args.expert}_{args.id}_{args.session}']
raw.interpolate_bads()

# Set the reference to average and immediately apply the projection
raw.set_eeg_reference('average', projection=True)
raw.apply_proj()

# Remove 50hz line noise and harmonics
# TODO: Is this needed?
raw.notch_filter([50, 100, 150, 200, 250], fir_design='firwin')

# Apply bandpass filter for 0.5, 40hz 
raw.filter(0.5, 40, method='fir', fir_design='firwin')

# Save the preprocessed data to a new file in MNE standard format
raw.save(out_path, overwrite=True)
