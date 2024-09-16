import os 
import numpy as np
import matplotlib.pyplot as plt

def load_single_connectivity(directory, id, preserved_epochs=False):
    if preserved_epochs:
        BL_NoG_path = os.path.join(directory, id, f'1_BL_NoG_epoch_connectivity.npy')
        BL_WiG_path = os.path.join(directory, id, f'1_BL_WiG_epoch_connectivity.npy')
        NoG_path = os.path.join(directory, id, f'2_NoG_epoch_connectivity.npy')
        WiG_path = os.path.join(directory, id, f'2_WiG_epoch_connectivity.npy')
    else:
        BL_NoG_path = os.path.join(directory, id, f'1_BL_NoG_connectivity.npy')
        BL_WiG_path = os.path.join(directory, id, f'1_BL_WiG_connectivity.npy')
        NoG_path = os.path.join(directory, id, f'2_NoG_connectivity.npy')
        WiG_path = os.path.join(directory, id, f'2_WiG_connectivity.npy')


    BL_NoG_data = np.load(BL_NoG_path)
    BL_WiG_data = np.load(BL_WiG_path)
    NoG_data = np.load(NoG_path)
    WiG_data = np.load(WiG_path)

    return BL_NoG_data, BL_WiG_data, NoG_data, WiG_data

def plot_single_connectivity(data, channel_names, title):
    fig, ax = plt.subplots()
    l = plt.imshow(data, cmap='viridis', aspect='auto')
    plt.colorbar(l)
    ax.set_xticks(np.arange(len(channel_names)))
    ax.set_yticks(np.arange(len(channel_names)))
    ax.set_xticklabels(channel_names)
    ax.set_yticklabels(channel_names)
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.show()

def average_single_over_freq_range(data, freqs, start, end):
    freqs_idx = [i for i, x in enumerate(freqs) if start <= x <= end]
    
    if len(data.shape) == 3:
        data = data[:, :, freqs_idx]
    else:
        data = data[:, :, :, freqs_idx]
    return np.mean(data, axis=-1)

def average_all_over_freq_range(data, freqs, start, end):
    return np.array([average_single_over_freq_range(data[i], freqs, start, end) for i in range(len(data))])

def load_all_connectivity(dir,preserved_epochs=False):
    ids = os.listdir(dir)

    all_BL_NoG = []
    all_BL_WiG = []
    all_NoG = []
    all_WiG = []
    for id in ids:
        try:
            BL_NoG_data, BL_WiG_data, NoG_data, WiG_data = load_single_connectivity(dir, id, preserved_epochs=preserved_epochs)
            all_BL_NoG.append(BL_NoG_data)
            all_BL_WiG.append(BL_WiG_data)
            all_NoG.append(NoG_data)
            all_WiG.append(WiG_data)
        except FileNotFoundError:
            print(f"Skipping {id} due to missing files")
            continue
        print(f"Loaded {id}")
    
    if preserved_epochs:
        all_BL_NoG = np.concatenate(all_BL_NoG, axis=0)
        all_BL_WiG = np.concatenate(all_BL_WiG, axis=0)
        all_NoG = np.concatenate(all_NoG, axis=0)
        all_WiG = np.concatenate(all_WiG, axis=0)

    all_BL_NoG = np.array(all_BL_NoG)
    all_BL_WiG = np.array(all_BL_WiG)
    all_NoG = np.array(all_NoG)
    all_WiG = np.array(all_WiG)

    return all_BL_NoG, all_BL_WiG, all_NoG, all_WiG

def calculate_cohens_d(group_1_mean, group_2_mean, group_1_std, group_2_std, group_1_n, group_2_n):
    pooled_std = np.sqrt(((group_1_n - 1) * group_1_std ** 2 + (group_2_n - 1) * group_2_std ** 2) / (group_1_n + group_2_n - 2))
    return (group_1_mean - group_2_mean) / pooled_std