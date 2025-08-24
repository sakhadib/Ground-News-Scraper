import subprocess
import os
import time  # Importing time module for the delay

# Get the current directory of this script
current_dir = os.path.dirname(os.path.realpath(__file__))


gn_sources = [
    ""
]


# Command to activate the virtual environment
activate_command = '.venv/Scripts/activate'

# Loop over each URL in the list
# Open terminal, activate the virtual environment, and run the command
try:
    # Start the subprocess to open terminal, activate virtual environment, and run commands sequentially
    for url in gn_sources:
        subprocess.run(f'cd {current_dir} && python g.py "{url}"', shell=True)
        time.sleep(1)
        subprocess.run("git add .", shell=True)
        subprocess.run(f"git commit -m 'Fetch news article {url}'", shell=True)
        time.sleep(1)  # Add 1 second delay between each URL
except Exception as e:
    print(f"Error: {e}")

