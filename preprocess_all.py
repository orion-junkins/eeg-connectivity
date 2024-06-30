# Run python preprocess.py expert 1 1 for all participants and sessions. 
import os

expert_ids = [1, 3]
novice_ids = [1, 4]
session_ids = [1,2]


for expert_id in expert_ids:
    for session_id in session_ids:
        print(f'Preprocessing expert {expert_id} session {session_id}')
        os.system(f'python preprocess.py expert {expert_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python preprocess.py"')

for novice_id in novice_ids:
    for session_id in session_ids:
        print(f'Preprocessing novice {novice_id} session {session_id}')
        os.system(f'python preprocess.py novice {novice_id} {session_id}')

        # Ensure the task is killed to free up resources
        os.system('pkill -f "python preprocess.py"')
