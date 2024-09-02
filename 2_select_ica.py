import mne 
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

np.random.seed(42)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Select ICA components for removal interactively")
    parser.add_argument('expert', type=str, help='Expert identifier')
    parser.add_argument('id', type=str, help='ID of the participant')
    parser.add_argument('session', type=str, help='Session number')
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg", help='Root directory of the data')
    parser.add_argument("--num_ica_comps", help="Number of ICA components", default=0.9999, type=float)

    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    expert = args.expert
    subject_id = args.id
    session = args.session
    num_ica_comps = args.num_ica_comps

    # Define input and output paths
    in_path = os.path.join(root_dir, 'preprocessed', expert, subject_id, f'{session}_raw.fif')
    ica_in_path = os.path.join(root_dir, 'ica', expert, subject_id, f'{session}_{num_ica_comps}_ica.fif')
    out_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_{num_ica_comps}_raw.fif')
    ica_drops_out_path = os.path.join(root_dir, 'processed', expert, subject_id, f'{session}_{num_ica_comps}_ica_drops.txt')

    # Make output dir
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Load the raw and ica data
    raw = mne.io.read_raw_fif(in_path, preload=True)
    ica = mne.preprocessing.read_ica(ica_in_path)

    # Use EOG channels to make a best guess of which ica comps to exclude as a starting point
    eog_inds, scores = ica.find_bads_eog(raw)
    ica.exclude = eog_inds

    # Plot the sources
    sources_obj = ica.plot_sources(raw, show_scrollbars=False)

    # Define the initial time window (in seconds)
    start_time = 0
    window_size = 10

    # Apply the ICA to the raw data
    raw_cleaned = raw.copy()
    ica.apply(raw_cleaned)
    data, times = raw[:]
    data_cleaned, _ = raw_cleaned[:]

    # Define the channels you want to plot
    channels_to_plot = ['Fpz', 'Fz', "AF3", "AF4", 'Cz', "POz", "HEOGR", "HEOGL", "VEOGU", "VEOGL"]  
    print(raw.ch_names)

    # Initial plot setup
    fig, ax = plt.subplots(len(channels_to_plot), 1, figsize=(10, 7))
    plt.subplots_adjust(bottom=0.25)

    def update_plot(val):
        start_time = slider.val
        start, stop = raw.time_as_index([start_time, start_time + window_size])

        for idx, channel_name in enumerate(channels_to_plot):
            ax[idx].clear()
            channel = raw.ch_names.index(channel_name)
            ax[idx].plot(times[start:stop], data[channel, start:stop], color='black', label='Original')
            ax[idx].plot(times[start:stop], data_cleaned[channel, start:stop], color='red', linestyle='--', label='Cleaned')

            ax[idx].set_ylabel(channel_name)
            ax[idx].set_xticks([])
            ax[idx].set_yticks([])
        
        ax[-1].set_xlabel('Time (s)')
        ax[0].legend()
        plt.suptitle(f'{expert} {subject_id} {session}')
        plt.draw()

    # Create a slider for time navigation
    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Time', 0, raw.times[-1] - window_size, valinit=start_time, valstep=1)
    slider.on_changed(update_plot)

    # Initial plot
    update_plot(start_time)

    # Add a button that triggers a reload of data
    def on_reload(event):
        nonlocal raw, ica, raw_cleaned, data, times, data_cleaned, sources_obj
        sources_obj.close()
        raw_cleaned = raw.copy()
        ica.apply(raw_cleaned)
        data, times = raw[:]
        data_cleaned, _ = raw_cleaned[:]
        sources_obj = ica.plot_sources(raw, show_scrollbars=False)
        update_plot(slider.val)

    ax_reload = plt.axes([0.4, 0.025, 0.1, 0.04])
    button_reload = Button(ax_reload, 'Reload')
    button_reload.on_clicked(on_reload)

    # Add a quit button
    def quit(event):
        plt.close()
        sources_obj.close()

    ax_quit = plt.axes([0.5, 0.025, 0.1, 0.04])
    button_quit = Button(ax_quit, 'Submit')
    button_quit.on_clicked(quit)

    # Move the figure to the right
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(1000, 0, 800, 1200)

    # Print the initial candidates alongside their scores
    print(f'Proposing dropping the following: {ica.exclude}')
    plt.show()

    ica.apply(raw_cleaned)

    # Save the data
    raw_cleaned.save(out_path, overwrite=True)

    # Write dropped ica components
    print(f'Dropping the following channels: {ica.exclude}')
    with open(ica_drops_out_path, 'w') as f:
        f.write("ICA Components Dropped: " + str(ica.exclude))

if __name__ == '__main__':
    main()