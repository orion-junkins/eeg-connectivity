## Directory Structure
Data is stored across three subdirectories within the `data` directory.

`data/raw-ant` contains the raw ANT Neuro Files. These cannot be read directly by MNE and thus must be loaded with EEGLab then re-saved as a generic `.set` and `.fdt` file pair. 

`data/raw` contains the resaved `.set` and `.fdt` files. This data is unprocessed and identical to the ANT Neuro files, just in a format that can be read by MNE. Note that these files **cannot** be renamed, since the `.set` file references the `.fdt` file by name. They **can** be moved to a new directory, so long as both files are kept together.

Every entry in data/raw is:
`data/raw/[expert, novice]_[id]_[recording]`

`data/processed` contains data that has been pre-processed. The pre-processing performed includes:
* Set Reference as the average
* FIR Band pass [0.5, 40] hz

## How to Process Data

### Raw ANT Neuro Files -> Raw .set and .fdt Files
1) Store relevant ANT Neuro Files (`.cnt`, `.evt` and `.seg`) in a single directory
2) Open EEG Lab via Matlab or via command line:
``` 
/Applications/EEGLAB/application/run_EEGLAB.sh /Applications/MATLAB/MATLAB_Runtime/R2022b/R2022b
```
3) Import the `.cnt` file (File > Import data > Using EEGLAB functions and plugins > From ANT EEGProbe .CNT file) 
4) Leave time interval blank > OK
5) Name it in the format `[expert, novice]_[id]_[recording #]` > OK
6) Add channel locations (Edit > Channel locations > Read locations > `data/channel_locs.elc` > Open > Autodetect > OK)
7) Save the dataset in `.set` format in the `raw` directory (File > Save current dataset as) using the same naming convention of `[expert, novice]_[id]_[recording #]`. This will create two files in the raw directory (`.set` for metadata and `.fdt` containing raw data values). These two files **cannot be renamed** and **must be kept in the same directory**.


### Raw .set and .fdt Files -> Processed

