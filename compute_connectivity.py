import mne 
import os
import numpy as np
from mne_connectivity import spectral_connectivity_time
import argparse
np.random.seed(42)

# Read command line argument for expert or novice, id and session, and number of components
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="Expert or Novice")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
parser.add_argument("--min_freq", help="Minimum frequency", default=0.5)
parser.add_argument("--max_freq", help="Maximum frequency", default=12.0)
args = parser.parse_args()

# Define the input and output paths
data_in_path = f'data/processed/{args.expert}_{args.id}_{args.session}_raw.fif'
data_out_path = f'data/connectivity/{args.expert}_{args.id}_{args.session}/'

# Load the raw data
raw = mne.io.read_raw_fif(data_in_path, preload=True)

# Isolate the event of interest
annotations = raw.annotations
onset_times = {annot['description']: annot['onset'] for annot in annotations}
start_time = onset_times["0, BL_NoG_beg###TEST"] + 2
end_time = onset_times["0, BL_NoG_end###TEST"] - 1
raw_cropped = raw.copy().crop(tmin=start_time, tmax=end_time)

# Isolate the frequency bands of interest
raw_delta = raw_cropped.copy().filter(l_freq=0.5, h_freq=4)

# Split into epochs
epochs = mne.make_fixed_length_epochs(raw_delta, duration=5.0, overlap=2.5, preload=True)

# Isolate the electrodes of interest: F3 (5),Fz (6),F4 (7),FCz (42),Cz (16),CP3 (48),CP4 (49),P1 (51),Pz (26),P2 (52),PPO1 (92) and PPO2 (93)
channels_of_interest = ["F3", "Fz", "F4", "FCz", "Cz", "CP3", "CP4", "P1", "Pz", "P2", "PPO1", "PPO2"]
indices_of_interest = [raw_cropped.ch_names.index(ch) for ch in channels_of_interest] # 0 indexed so 1 less than above
epochs.pick(indices_of_interest)

# Define the frequency intervals to study
min = float(args.min_freq)
max = float(args.max_freq)
num_intervals = int((max-min) * 2) + 1
freqs = np.linspace(min, max, num_intervals)
n_cycles = freqs / 2.0

# Compute the spectral connectivity
spec_con_obj = spectral_connectivity_time(epochs, freqs=freqs, method='plv', mode='multitaper', n_cycles=n_cycles, average=True)
arr = spec_con_obj.get_data(output="dense")
data = arr

# Make out dir if needed
os.makedirs(data_out_path, exist_ok=True)

# Store the connectivity array as a numpy array in the output path
np.save(data_out_path + "connectivity.npy", arr)

# Save the channel names for reference
np.save(data_out_path + 'channel_names.npy', channels_of_interest)

# Save the frequencies used for reference
np.save(data_out_path + 'frequencies.npy', freqs)