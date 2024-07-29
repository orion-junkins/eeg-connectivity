python 0_mark_bads.py expert 5b 2 --root_dir data2
python 0_mark_bads.py novice 6 2 --root_dir data2
python 0_mark_bads.py novice 5b 2 --root_dir data2

python 1_preproc.py expert 5b 2 --root_dir data2
python 1_preproc.py novice 6 2 --root_dir data2
python 1_preproc.py novice 5b 2 --root_dir data2

python 2_select_ica.py expert 5b 2 --root_dir data2
python 2_select_ica.py novice 6 2 --root_dir data2
python 2_select_ica.py novice 5b 2 --root_dir data2

python 3_compute_connectivity.py expert 5b 2 --root_dir data2 --min_freq 0.5 --max_freq 12.0
python 3_compute_connectivity.py novice 6 2 --root_dir data2 --min_freq 0.5 --max_freq 12.0
python 3_compute_connectivity.py novice 5b 2 --root_dir data2 --min_freq 0.5 --max_freq 12.0

python 4_plot_connectivity.py expert 5b 2 --root_dir data2
python 4_plot_connectivity.py novice 6 2 --root_dir data2
python 4_plot_connectivity.py novice 5b 2 --root_dir data2
