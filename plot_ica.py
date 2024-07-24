#%%
import mne 
import numpy as np
import argparse
import mne
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
np.random.seed(42)
plt.ion()

# Read command line argument for expert or novice, id and session, and number of components
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="Expert or Novice")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
parser.add_argument("--num_components", help="Number of ICA components", default=24, type=int)
parser.add_argument("--show_fp1", help="Show Fp1 channel before and after removal", default=False, action='store_true')
args = parser.parse_args(
)
expert = args.expert
id = args.id
session = args.session
num_components = args.num_components


# Define the input and output paths
data_in_path = f'data/preprocessed/{expert}_{id}_{session}_raw.fif'
data_out_path = f'data/processed/{expert}_{id}_{session}_raw.fif'
ica_path = f'data/ica/{expert}_{id}_{session}_{num_components}_ica.fif'

# Load the data and ICA
raw = mne.io.read_raw_fif(data_in_path, preload=True)
ica = mne.preprocessing.read_ica(ica_path)


print("ICA Exclude before: ", ica.exclude)
ica.plot_components(inst=raw)


# Wait for keypress
input("Press Enter to continue...")

print("ICA Exclude after: ", ica.exclude)

# Save the ica object
ica.save(ica_path, overwrite=True)
