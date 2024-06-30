import mne 
import numpy as np
import argparse
np.random.seed(42)

# Read command line argument for expert or novice, id and session, and number of components
parser = argparse.ArgumentParser()
parser.add_argument("expert", help="Expert or Novice")
parser.add_argument("id", help="ID of the participant")
parser.add_argument("session", help="Session number")
parser.add_argument("--show_fp1", help="Show Fp1 channel before and after removal", default=False, action='store_true')
args = parser.parse_args(
)

# Define the input and output paths
data_in_path = f'data/preprocessed/{args.expert}_{args.id}_{args.session}_raw.fif'
data_out_path = f'data/processed/{args.expert}_{args.id}_{args.session}_raw.fif'
ica_path = f'data/ica/{args.expert}_{args.id}_{args.session}_ica.fif'

# Load the data and ICA
raw = mne.io.read_raw_fif(data_in_path, preload=True)
ica = mne.preprocessing.read_ica(ica_path)


# Plot the fp1 channel to visualize before and after
if args.show_fp1:
    raw.plot(start=0, duration=10, n_channels=1, picks=['Fp1'])

# Plot the ICA components
ica.plot_sources(raw, show_scrollbars=False)

# Pause for user input
input("Select components to remove and press enter to continue...")

# Print which components will be removed
print(f'Removing components: {ica.exclude}')

# Remove the selected components
ica.apply(raw)

# Plot the fp1 channel to visualize before and after
if args.show_fp1:
    raw.plot(start=0, duration=10, n_channels=1, picks=['Fp1'])
    input("Press enter to continue...")

# Save the data
raw.save(data_out_path, overwrite=True)
