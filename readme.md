# EEG Connectivity in Cognitively Challenging Tasks
### ETH Zurich Practical Work - Orion Junkins
#### Supervised by Dr. Hanna Poikonen and Dr. Christian Holz
This repository explores connectivity metrics in EEG data collected from experts and novices performing cognitively challenging mathematical tasks.

Raw data was collected using ANT Neuro and is initially stored in their proprietary data format.

A series of scripts perform preprocessing on the data ultimately yielding a matrices of connectivity metrics for various frequency bands. While only these final matrices are needed for comparison, data is saved at several points along the way to enable faster experimentation in later stages without recomputing earlier stages.

The following list outlines the processing procedure, highlighting the relevant directories for intermediary data.

## 1) Handling Ant Neuro Files
### ```data/raw-ant``` -> ```data/raw```
The Raw Ant Neuro files in ```data/raw-ant``` cannot be read directly by MNE and thus must be loaded with EEGLab then re-saved as a generic `.set` and `.fdt` file pair. 

`data/raw` contains the resaved `.set` and `.fdt` files. This data is unprocessed and identical to the ANT Neuro files, just in a format that can be read by MNE. Note that these files **cannot** be renamed, since the `.set` file references the `.fdt` file by name. They **can** be moved to a new directory, so long as both files are kept together.

## 2) Preprocessing
### ```data/raw``` -> ```data/preprocessed```
Generic preprocessing is performed including:
* Resample to 512 hz
* Interpolate bad channels
* Set Reference as the average
* Notch filter for 50hz line noise
* FIR Band pass [0.5, 40] hz

A single recording can be preprocessed as follows:

```bash 
python preprocess.py <expert> <id> <session>
```
Where `<expert>` is either "expert" or "novice" and `<id>` and `<session>` are both integers.

Alternatively, multiple recordings can be preprocessed at once as follows:
```bash
python preprocess_all.py
```

Ranges of expert ids, novice ids, and session ids are hard coded in the python script and can be tuned there as needed.


## 3) ICA
### ```data/preprocessed``` -> ```data/ica``` and ```data/processed```
ICA is fit and then manually inspected to identify and remove unwanted components. Because fitting is time intensive, these two stages are separated.

First, fit ica. To fit a single recording:

```bash
python fit_ica.py <expert> <id> <session> [--num_components NUM_COMPONENTS]
```

`num_components` is an integer specifying the number of ica components to use and other arguments behave the same as in `preprocess.py`.
To fit multiple at once:

```bash
fit_ica_all.py
```

This will generate `.fif` files in ```data/ica``` allowing rapid loading.

Second, identify the components to remove. To work on a single recording:

```bash
python remove_ica.py [--num_components NUM_COMPONENTS] [--show_fp1] <expert> <id> <session>
```

This script opens an interactive plot of ICA components for manual flagging of unwanted components.`num_components` must match the number previously fit. `show_fp1` is an additional flag that enables displaying before and after plots of the `Fp1` channel.

As in prior stages, multiple recordings can be handled at once using:
```bash
python remove_ica_all.py
```

## 4) Connectivity Computation (WIP)
### ```data/processed``` -> ```data/connectivity```
Using the processed data, compute the Phase Locking Value for the electrodes fo interest.

```bash
python compute_connectivity.py <expert> <id> <session> [--min_freq MIN_FREQ] [--max_freq MAX_FREQ]
```

min_freq and max_freq specify the lower and upper bound frequencies to compute PLV for. PLV will be computed for every value in between in 0.5 hz increments.

This script will save three ```.npy``` files in ```data/connectivity/<expert>_<id>_<session>/``` to retain channel names, connectivity scores and frequency intervals.

```plot_connectivity.ipynb``` provides an interactive playground for visualizing and experimenting with connectivity scores. It loads the three ```.npy``` files and provides basic plotting functionality.


