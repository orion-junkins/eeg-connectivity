import mne 
import os
import numpy as np
from mne.preprocessing import ICA
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity.viz import plot_connectivity_circle
import argparse
np.random.seed(42)

# Read command line argument for expert or novice, id and session, and number of components
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="Expert or Novice")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
parser.add_argument("--num_components", help="Number of ICA components", default=24, type=int)

args = parser.parse_args()


# Define the input and output paths
data_in_path = f'data/processed/{args.expert}_{args.id}_{args.session}_raw.fif'
data_out_path = f'data/connectivity/{args.expert}_{args.id}_{args.session}/'


raw = mne.io.read_raw_fif(data_in_path, preload=True)

# Isolate the event of interest
annotations = raw.annotations
onset_times = {annot['description']: annot['onset'] for annot in annotations}
start_time = onset_times["0, BL_NoG_beg###TEST"] + 2
end_time = onset_times["0, BL_NoG_end###TEST"] - 1
raw_cropped = raw.copy().crop(tmin=start_time, tmax=end_time)



# Isolate the frequency bands of interest
raw_delta = raw_cropped.copy().filter(l_freq=0.5, h_freq=4)


# Calculate the connectivity array
def get_connectivity_arr(raw_cropped):
    epochs = mne.make_fixed_length_epochs(raw_cropped, duration=5.0, overlap=2.5, preload=True)
    # Calculate and plot the connectivity
    SpectralConnectivity_object = spectral_connectivity_epochs(epochs, method='plv', mode='multitaper', sfreq=raw.info['sfreq'], fmin=0.5, fmax=4, faverage=True, mt_adaptive=False, n_jobs=1)
    arr = (SpectralConnectivity_object.get_data(output="dense"))[:,:,0]
    return arr


arr = get_connectivity_arr(raw_delta)

# Make out dir if needed
os.makedirs(data_out_path, exist_ok=True)

# Store the connectivity array as a numpy array in the output path
np.save(data_out_path + 'delta.npy', arr)


# Save the channel names for reference
channel_names = raw_delta.ch_names
np.save(data_out_path + 'channel_names.npy', channel_names)
