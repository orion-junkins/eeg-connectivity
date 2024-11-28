import numpy as np
import os 
from collections import defaultdict
# Define a dataset class that takes in a path to a connectivity dir in init
class Dataset:
    def __init__(self, connectivity_dir_path, root_dir="/Volumes/eeg", frequency_file="frequencies.npy", electrode_file="electrode_names.npy", novice_excludes=[], expert_excludes=[], entropy_analysis=False):
        self.directory = os.path.join(root_dir, connectivity_dir_path)
        self.frequencies = np.load(os.path.join(root_dir, frequency_file))
        self.electrode_names = np.load(os.path.join(root_dir, electrode_file))
        self.novice_excludes = novice_excludes
        self.expert_excludes = expert_excludes
        self.entropy_analysis = entropy_analysis

        self.id_dicts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
        self.lists = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.numpy_arrays = defaultdict(lambda: defaultdict(lambda: defaultdict(None)))

        self.load_all_id_dicts()
        self.load_all_lists()
        self.load_all_numpy_arrays()


    def load_all_id_dicts(self):
        # Create a dict of all raw subjects using _load_invidiual_subject()
        for group_dir in ['expert', 'novice']:
            group_dir_path = os.path.join(self.directory, group_dir)
            ids = os.listdir(group_dir_path)

            for id in ids:
                if group_dir == 'expert' and id in self.expert_excludes:
                    continue
                if group_dir == 'novice' and id in self.novice_excludes:
                    continue
                # If id is not a directory, skip
                if not os.path.isdir(os.path.join(group_dir_path, id)):
                    continue
                BL_NoG_data, BL_WiG_data, NoG_data, WiG_data = [], [], [], []
                try:
                    BL_NoG_data, BL_WiG_data, NoG_data, WiG_data = self._load_invidiual_subject(group_dir, id)
                    self.id_dicts[group_dir]["BL"]["NoG"][id] = BL_NoG_data
                    self.id_dicts[group_dir]["demo"]["NoG"][id] = NoG_data
                    self.id_dicts[group_dir]["BL"]["WiG"][id] = BL_WiG_data
                    self.id_dicts[group_dir]["demo"]["WiG"][id] = WiG_data
                except FileNotFoundError:
                    continue

    def load_all_lists(self):
        for group in self.id_dicts.keys():
            for demo in self.id_dicts[group].keys():
                for gestures in self.id_dicts[group][demo].keys():
                    ids = list(self.id_dicts[group][demo][gestures].keys())
                    data_as_list = []
                    for id in ids:
                        data_as_list.append(self.id_dicts[group][demo][gestures][id])
                    self.lists[group][demo][gestures] = data_as_list


    def load_all_numpy_arrays(self):
        for group in self.lists.keys():
            for demo in self.lists[group].keys():
                for gestures in self.lists[group][demo].keys():
                    averaged_data= []
                    for subject in self.lists[group][demo][gestures]:
                        # Average the data for each subject over the first dimension
                        subject_averaged = np.mean(subject, axis=0)
                        averaged_data.append(subject_averaged)
                    self.numpy_arrays[group][demo][gestures] = np.array(averaged_data)
    
    def get_frequency_average_bounds(self, group, demo, gestures, min_freq, max_freq):
        data = self.numpy_arrays[group][demo][gestures]
        frequency_indices = np.where((self.frequencies >= min_freq) & (self.frequencies <= max_freq))[0]

        data = data[:, :, :, frequency_indices]

        return np.mean(data, axis=3)
    
    def get_frequency_average(self, group, demo, gestures, freq):
        # Check if we are just storing shannon entorpy, in which case we can direclty return the array at the corresponding index without averaging
        if self.entropy_analysis:
            if freq == "delta":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 0]
            if freq == "theta":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 1]
            if freq == "low alpha":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 2]
            if freq == "high alpha":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 3]
            if freq == "low beta":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 4]
            if freq == "high beta":
                return self.numpy_arrays[group][demo][gestures][:, :, :, 5]
        else:
            if freq == "delta":
                return self.get_frequency_average_bounds(group, demo, gestures, 0.5, 4)
            if freq == "theta":
                return self.get_frequency_average_bounds(group, demo, gestures, 4, 8)
            if freq == "low alpha":
                return self.get_frequency_average_bounds(group, demo, gestures, 8, 10)
            if freq == "high alpha":
                return self.get_frequency_average_bounds(group, demo, gestures, 10, 13)
            if freq == "low beta":
                return self.get_frequency_average_bounds(group, demo, gestures, 13, 20)
            if freq == "high beta":
                return self.get_frequency_average_bounds(group, demo, gestures, 20, 30)


    
    def _load_invidiual_subject(self, group_dir, id):
            path_BL_NoG = os.path.join(self.directory, group_dir, id, f'BL_NoG_connectivity.npy')
            path_BL_WiG = os.path.join(self.directory, group_dir, id, f'BL_WiG_connectivity.npy')
            path_NoG = os.path.join(self.directory, group_dir, id, f'NoG_connectivity.npy')
            path_WiG = os.path.join(self.directory, group_dir, id, f'WiG_connectivity.npy')

            BL_NoG_data = np.load(path_BL_NoG)
            BL_WiG_data = np.load(path_BL_WiG)
            NoG_data = np.load(path_NoG)
            WiG_data = np.load(path_WiG)

            return BL_NoG_data, BL_WiG_data, NoG_data, WiG_data
    
    def get_electrode_idx(self, electrode_name):
        # Get the index for a particular electrode
        return np.where(self.electrode_names == electrode_name)[0][0]
    
    def get_frequency_average_for_electrode_pair(self, group, demo, gestures, freq, electrode1, electrode2):
        arr = self.get_frequency_average(group, demo, gestures, freq)

        if type(electrode1) == str:
            electrode1_idx = self.get_electrode_idx(electrode1)
        else:
            electrode1_idx = electrode1
        if type(electrode2) == str:
            electrode2_idx = self.get_electrode_idx(electrode2)
        else:
            electrode2_idx = electrode2

        if electrode1_idx < electrode2_idx:
            electrode1_idx, electrode2_idx = electrode2_idx, electrode1_idx

        print(electrode1_idx, electrode2_idx)
        return arr[:, electrode1_idx, electrode2_idx]
