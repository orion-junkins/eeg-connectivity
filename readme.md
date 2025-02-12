# Gesticulation while Explaining Complex Mathematics
## Orion Junkins
#### ETH Zurich Practical Work 
#### Supervised by Dr. Hanna Poikonen and Dr. Christian Holz
This repository explores connectivity metrics in EEG data collected from experts and novices performing cognitively challenging mathematical tasks both with and without free gesticulation.

The full written report is available in [Report.pdf](https://github.com/orion-junkins/eeg-connectivity/blob/main/Report.pdf). This document provides a top level overview of the context, purpose and results of this work. It serves as a companion document to this codebase. To reproduce and/or extend this work, it is advised to explore the report and the codebase side by side. At several points, the report references files that are relevant to a particular section.

This codebase and report are provided side by side in the spirit of open science. Care has been taken to ensure that this work is easily reproducible and extendable. In particular, note the following:

- All preprocessed data is provided in [data/connectivity_scores_entropy_5s](https://github.com/orion-junkins/eeg-connectivity/tree/main/data/connectivity_scores_entropy_5s). These numpy arrays are the result of the preprocessing procedure described in the report. They are an ideal starting point for a range of analyses beyond what is performed in this work.

- A dataset tutorial is provided in [extension_tutorial.ipynb](https://github.com/orion-junkins/eeg-connectivity/blob/main/extension_tutorial.ipynb). This notebook gives a basic introduction to the format of the data and the `Dataset` class that provides convenient access to various subsets.

- All results described in the paper are produced with (and can be reproduced with) [results_reproduction.ipynb](https://github.com/orion-junkins/eeg-connectivity/blob/main/results_reproduction.ipynb). This notebook directly generates the LaTeX and figures that appear in the results section.

