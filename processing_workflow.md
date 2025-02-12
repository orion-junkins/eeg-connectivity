# Processing Workflow
This document describes the methodology for generating the final numpy arrays of processed connectivity metric data. This workflow assumes access to the underlying raw data (initially stored in the proprietary Ant Neuro format).

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

## 3) ICA
### ```data/preprocessed``` -> ```data/ica``` and ```data/processed```
ICA is fit and then manually inspected to identify and remove unwanted components. Because fitting is time intensive, these two stages are separated.

First, fit ica. To fit a single recording:

```bash
python fit_ica.py <expert> <id> <session> [--num_components NUM_COMPONENTS]
```

`num_components` is an integer specifying the number of ica components to use OR the percent of variance to be explained by the chosen components. Other arguments behave the same as in `preprocess.py`.

This will generate `.fif` files in ```data/ica``` allowing rapid loading.

Second, identify the components to remove:

```bash
python remove_ica.py [--num_components NUM_COMPONENTS] [--show_fp1] <expert> <id> <session>
```

This script opens an interactive plot of ICA components for manual flagging of unwanted components.`num_components` must match the number previously fit. `show_fp1` is an additional flag that enables displaying before and after plots of the `Fp1` channel.


## 4) Connectivity Computation (WIP)
### ```data/processed``` -> ```data/connectivity```
Using the processed data, compute the synchrony index for the electrodes fo interest.

```bash
python compute_connectivity_entropy.py <expert> <id>
```

`compute_connectivity_entropy` exposes many command line arguments to control which subset of data is used (WiG or NoG, Demo or Baseline), and how the epoching is performed (duration and overlap).

This script will save a ```.npy``` file containing the array of calculated synchrony values.