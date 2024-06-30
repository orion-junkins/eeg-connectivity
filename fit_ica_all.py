# Run python fit_ica.py for multiple participants and sessions.
import os

expert_ids = [1, 3]
novice_ids = [1, 4]
session_ids = [1]

num_ica_components = 24

for expert_id in expert_ids:
    for session_id in session_ids:
        print(f'Fiting ICA for expert {expert_id} session {session_id}')
        os.system(f'python fit_ica.py expert {expert_id} {session_id} --num_components {num_ica_components}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python fit_ica.py"')

for novice_id in novice_ids:
    for session_id in session_ids:
        print(f'Fitting ICA for novice {novice_id} session {session_id}')
        os.system(f'python fit_ica.py novice {novice_id} {session_id} --num_components {num_ica_components}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python fit_ica.py"')
