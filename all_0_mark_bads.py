import subprocess
import argparse
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Call EEG processing script for each .set file")
    parser.add_argument('--root_dir', type=str, default="/Volumes/eeg/", help='Root directory of the data')
    parser.add_argument('--script', type=str, default='0_mark_bads.py', help='Path to the EEG processing script')

    # Parse arguments
    args = parser.parse_args()
    root_dir = args.root_dir
    script_path = args.script

    # Traverse the directory and find all .set files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".set"):
                # Extract expert, subject_id, and session from the file path
                path_parts = root.split(os.sep)
                if len(path_parts) < 3:
                    continue  # Skip directories that don't match the expected structure
                expert = path_parts[-2]
                subject_id = path_parts[-1]
                session = os.path.splitext(file)[0]

                # Construct the command and call the EEG processing script
                command = [
                    'python', script_path,
                    expert,
                    subject_id,
                    session,
                    '--root_dir', root_dir
                ]
                print("command:", command)
                subprocess.run(command)

if __name__ == '__main__':
    main()