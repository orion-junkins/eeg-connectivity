import mne 
import numpy as np
from mne.preprocessing import ICA
import argparse
np.random.seed(42)

# Read command line argument for expert or novice, id and session, and number of components
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="Expert or Novice")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
args = parser.parse_args()

data_in_path = f'data/preprocessed/{args.expert}_{args.id}_{args.session}_raw.fif'
data_out_path = f'data/processed/{args.expert}_{args.id}_{args.session}_raw.fif'
ica_path = f'data/ica/{args.expert}_{args.id}_{args.session}_ica.fif'

raw = mne.io.read_raw_fif(data_in_path, preload=True)
ica = mne.preprocessing.read_ica(ica_path)

raw.plot()

ica.plot_sources(raw, show_scrollbars=False)

# Pause for user input
input("Select components to remove and press enter to continue...")

# Print which components will be removed
print(f'Removing components: {ica.exclude}')

# Remove the selected components
ica.apply(raw)

# Save the data
raw.save(data_out_path, overwrite=True)

