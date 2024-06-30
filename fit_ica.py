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
parser.add_argument("--num_components", help="Number of ICA components", default=20, type=int)

args = parser.parse_args()

# Define paths
in_path = f'data/preprocessed/{args.expert}_{args.id}_{args.session}_raw.fif'
out_path = f'data/ica/{args.expert}_{args.id}_{args.session}_{args.num_components}_ica.fif'

# Load the preprocessed data
raw = mne.io.read_raw_fif(in_path, preload=True)

# Initialize ICA object
ica = ICA(n_components=args.num_components, random_state=42)

# Fit the ICA to the data
ica.fit(raw)

# Save the ICA object
ica.save(out_path, overwrite=True)
