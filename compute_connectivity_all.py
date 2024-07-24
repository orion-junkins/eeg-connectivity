# Run python compute_connectivity.py for multiple participants and sessions. 
import os

expert_ids = [1, 3]
novice_ids = [1, 4]
session_ids = [1]


for expert_id in expert_ids:
    for session_id in session_ids:
        print(f'Computing Connectivity for expert {expert_id} session {session_id}')
        os.system(f'python compute_connectivity.py expert {expert_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python compute_connectivity.py"')

for novice_id in novice_ids:
    for session_id in session_ids:
        print(f'Computing Connectivity for novice {novice_id} session {session_id}')
        os.system(f'python compute_connectivity.py novice {novice_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python compute_connectivity.py"')
