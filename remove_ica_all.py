# Run python remove_ica.py for all participants and sessions. 
import os

expert_ids = [1, 3]
novice_ids = [1, 4]
session_ids = [1]


for expert_id in expert_ids:
    for session_id in session_ids:
        print(f'Running interactive ICA removal for expert {expert_id} session {session_id}')
        os.system(f'python remove_ica.py expert {expert_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python remove_ica.py"')

for novice_id in novice_ids:
    for session_id in session_ids:
        print(f'Running interactive ICA removal for novice {novice_id} session {session_id}')
        os.system(f'python remove_ica.py novice {novice_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python remove_ica.py"')
