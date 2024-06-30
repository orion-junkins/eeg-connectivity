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

